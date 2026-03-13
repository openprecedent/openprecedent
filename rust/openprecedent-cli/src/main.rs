use std::collections::HashSet;
use std::ffi::OsString;
use std::fs::File;
use std::io::{BufRead, BufReader};

use chrono::{DateTime, Utc};
use clap::{ArgAction, Args, CommandFactory, FromArgMatches, Parser, Subcommand};
use openprecedent_capture_openclaw as capture_openclaw;
use openprecedent_contracts::{
    Artifact, ArtifactType, Case, CaseStatus, Decision, DecisionExplanation, DecisionType, Event,
    EventActor, EventType, OutputFormat, PathsDoctorReport, Precedent, ReplayResponse,
    StorageDoctorReport, VersionReport, CLI_BINARY_NAME, CONTRACT_PHASE,
};
use openprecedent_core::{
    build_environment_report, build_paths_report, build_storage_report, build_version_report,
    not_implemented, resolve_runtime_config, CliConfigOverrides, ResolvedRuntimeConfig,
};
use openprecedent_store_sqlite::SqliteStore;
use serde::Deserialize;
use serde::Serialize;
use serde_json::{Map, Value};
use uuid::Uuid;

#[derive(Debug, Serialize)]
struct CaptureImportOutput {
    case: Case,
    imported_event_count: usize,
    events: Vec<Event>,
}

#[derive(Debug, Serialize)]
struct OpenClawSessionImportOutput {
    case: Case,
    transcript_path: String,
    imported_event_count: usize,
    unsupported_record_type_counts: std::collections::BTreeMap<String, usize>,
    events: Vec<Event>,
}

#[derive(Debug, Parser)]
#[command(name = CLI_BINARY_NAME)]
#[command(about = "Stable public CLI for OpenPrecedent")]
struct Cli {
    #[arg(long, global = true, value_enum)]
    format: Option<OutputFormat>,
    #[arg(long, global = true)]
    home: Option<std::path::PathBuf>,
    #[arg(long, global = true)]
    db: Option<std::path::PathBuf>,
    #[arg(long = "invocation-log", global = true)]
    invocation_log: Option<std::path::PathBuf>,
    #[arg(long = "state-file", global = true)]
    state_file: Option<std::path::PathBuf>,
    #[arg(long, global = true)]
    config: Option<std::path::PathBuf>,
    #[arg(long = "no-color", global = true, action = ArgAction::SetTrue)]
    no_color: bool,
    #[command(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    Case(CaseCommand),
    Event(EventCommand),
    Decision(DecisionCommand),
    Replay(ReplayCommand),
    Precedent(PrecedentCommand),
    Capture(CaptureCommand),
    Lineage(LineageCommand),
    Eval(EvalCommand),
    Doctor(DoctorCommand),
    Version,
}

#[derive(Debug, Args)]
struct CaseCommand {
    #[command(subcommand)]
    command: CaseSubcommand,
}

#[derive(Debug, Subcommand)]
enum CaseSubcommand {
    Create(CreateCaseArgs),
    List,
    Show(ShowCaseArgs),
}

#[derive(Debug, Args)]
struct CreateCaseArgs {
    #[arg(long)]
    title: String,
    #[arg(long = "case-id")]
    case_id: Option<String>,
    #[arg(long = "user-id")]
    user_id: Option<String>,
    #[arg(long = "agent-id")]
    agent_id: Option<String>,
}

#[derive(Debug, Args)]
struct ShowCaseArgs {
    case_id: String,
}

#[derive(Debug, Args)]
struct EventCommand {
    #[command(subcommand)]
    command: EventSubcommand,
}

#[derive(Debug, Subcommand)]
enum EventSubcommand {
    Append(AppendEventArgs),
    ImportJsonl(ImportJsonlArgs),
}

#[derive(Debug, Args)]
struct AppendEventArgs {
    case_id: String,
    event_type: String,
    actor: String,
    #[arg(long, default_value = "{}")]
    payload: String,
    #[arg(long = "event-id")]
    event_id: Option<String>,
}

#[derive(Debug, Args)]
struct ImportJsonlArgs {
    path: std::path::PathBuf,
    #[arg(long = "case-id")]
    case_id: Option<String>,
}

#[derive(Debug, Args)]
struct DecisionCommand {
    #[command(subcommand)]
    command: DecisionSubcommand,
}

#[derive(Debug, Subcommand)]
enum DecisionSubcommand {
    Extract(DecisionCaseArgs),
    List(DecisionCaseArgs),
}

#[derive(Debug, Args)]
struct DecisionCaseArgs {
    case_id: String,
}

#[derive(Debug, Args)]
struct ReplayCommand {
    #[command(subcommand)]
    command: ReplaySubcommand,
}

#[derive(Debug, Subcommand)]
enum ReplaySubcommand {
    Case(ReplayCaseArgs),
}

#[derive(Debug, Args)]
struct ReplayCaseArgs {
    case_id: String,
}

#[derive(Debug, Args)]
struct PrecedentCommand {
    #[command(subcommand)]
    command: PrecedentSubcommand,
}

#[derive(Debug, Subcommand)]
enum PrecedentSubcommand {
    Find(PrecedentFindArgs),
}

#[derive(Debug, Args)]
struct PrecedentFindArgs {
    case_id: String,
    #[arg(long, default_value_t = 3)]
    limit: usize,
}

#[derive(Debug, Args)]
struct CaptureCommand {
    #[command(subcommand)]
    runtime: CaptureRuntime,
}

#[derive(Debug, Subcommand)]
enum CaptureRuntime {
    Openclaw(OpenclawCaptureCommand),
    Codex(CodexCaptureCommand),
}

#[derive(Debug, Args)]
struct OpenclawCaptureCommand {
    #[command(subcommand)]
    command: OpenclawCaptureSubcommand,
}

#[derive(Debug, Subcommand)]
enum OpenclawCaptureSubcommand {
    ListSessions(OpenClawListSessionsArgs),
    ImportSession(OpenClawImportSessionArgs),
    CollectSessions(OpenClawCollectSessionsArgs),
    ImportJsonl(OpenClawImportJsonlArgs),
}

#[derive(Debug, Args)]
struct OpenClawListSessionsArgs {
    #[arg(long = "sessions-root")]
    sessions_root: Option<std::path::PathBuf>,
    #[arg(long, default_value_t = 10)]
    limit: usize,
}

#[derive(Debug, Args)]
struct OpenClawImportJsonlArgs {
    path: std::path::PathBuf,
    #[arg(long = "case-id")]
    case_id: String,
    #[arg(long)]
    title: String,
    #[arg(long = "user-id")]
    user_id: Option<String>,
    #[arg(long = "agent-id", default_value = "openclaw")]
    agent_id: String,
}

#[derive(Debug, Args)]
struct OpenClawImportSessionArgs {
    #[arg(long = "session-file")]
    session_file: Option<std::path::PathBuf>,
    #[arg(long = "session-id")]
    session_id: Option<String>,
    #[arg(long)]
    latest: bool,
    #[arg(long = "sessions-root")]
    sessions_root: Option<std::path::PathBuf>,
    #[arg(long = "case-id")]
    case_id: String,
    #[arg(long)]
    title: Option<String>,
    #[arg(long = "user-id")]
    user_id: Option<String>,
    #[arg(long = "agent-id", default_value = "openclaw")]
    agent_id: String,
}

#[derive(Debug, Args)]
struct OpenClawCollectSessionsArgs {
    #[arg(long = "sessions-root")]
    sessions_root: Option<std::path::PathBuf>,
    #[arg(long = "state-file")]
    state_file: Option<std::path::PathBuf>,
    #[arg(long, default_value_t = 1)]
    limit: usize,
    #[arg(long = "user-id")]
    user_id: Option<String>,
    #[arg(long = "agent-id", default_value = "openclaw")]
    agent_id: String,
}

#[derive(Debug, Args)]
struct CodexCaptureCommand {
    #[command(subcommand)]
    command: CodexCaptureSubcommand,
}

#[derive(Debug, Subcommand)]
enum CodexCaptureSubcommand {
    ImportRollout(TrailingArgs),
}

#[derive(Debug, Args)]
struct LineageCommand {
    #[command(subcommand)]
    command: LineageSubcommand,
}

#[derive(Debug, Subcommand)]
enum LineageSubcommand {
    Brief(TrailingArgs),
    Invocation(LineageInvocationCommand),
}

#[derive(Debug, Args)]
struct LineageInvocationCommand {
    #[command(subcommand)]
    command: LineageInvocationSubcommand,
}

#[derive(Debug, Subcommand)]
enum LineageInvocationSubcommand {
    List(TrailingArgs),
    Inspect(TrailingArgs),
}

#[derive(Debug, Args)]
struct EvalCommand {
    #[command(subcommand)]
    command: EvalSubcommand,
}

#[derive(Debug, Subcommand)]
enum EvalSubcommand {
    Fixtures(TrailingArgs),
    CapturedOpenclawSessions(TrailingArgs),
}

#[derive(Debug, Args)]
struct DoctorCommand {
    #[command(subcommand)]
    command: DoctorSubcommand,
}

#[derive(Debug, Subcommand)]
enum DoctorSubcommand {
    Paths,
    Storage,
    Environment,
}

#[derive(Debug, Args)]
struct TrailingArgs {
    #[arg(trailing_var_arg = true)]
    args: Vec<OsString>,
}

fn main() {
    std::process::exit(main_from(std::env::args_os()));
}

fn main_from<I, T>(args: I) -> i32
where
    I: IntoIterator<Item = T>,
    T: Into<OsString> + Clone,
{
    let matches = Cli::command().get_matches_from(args);
    let cli = match Cli::from_arg_matches(&matches) {
        Ok(cli) => cli,
        Err(error) => {
            eprintln!("{error}");
            return 2;
        }
    };

    let config = match resolve_runtime_config(&CliConfigOverrides {
        format: cli.format,
        no_color: cli.no_color,
        home: cli.home.clone(),
        db: cli.db.clone(),
        invocation_log: cli.invocation_log.clone(),
        state_file: cli.state_file.clone(),
        config: cli.config.clone(),
    }) {
        Ok(config) => config,
        Err(error) => {
            eprintln!("{error}");
            return 1;
        }
    };

    match cli.command {
        Command::Doctor(command) => match command.command {
            DoctorSubcommand::Paths => render(&build_paths_report(&config), config.format.value),
            DoctorSubcommand::Storage => {
                render(&build_storage_report(&config), config.format.value)
            }
            DoctorSubcommand::Environment => {
                render(&build_environment_report(&config), config.format.value)
            }
        },
        Command::Version => render(
            &build_version_report(env!("CARGO_PKG_VERSION"), CONTRACT_PHASE),
            config.format.value,
        ),
        Command::Case(command) => handle_case(command, &config),
        Command::Event(command) => handle_event(command, &config),
        Command::Decision(command) => handle_decision(command, &config),
        Command::Replay(command) => handle_replay(command, &config),
        Command::Precedent(command) => handle_precedent(command, &config),
        Command::Capture(command) => handle_capture(command, &config),
        Command::Lineage(command) => render_not_implemented_path(lineage_path(command)),
        Command::Eval(command) => render_not_implemented_path(eval_path(command)),
    }
}

fn handle_case(command: CaseCommand, config: &ResolvedRuntimeConfig) -> i32 {
    let store = match SqliteStore::new(&config.db.path) {
        Ok(store) => store,
        Err(error) => {
            eprintln!("{error}");
            return 1;
        }
    };

    match command.command {
        CaseSubcommand::Create(args) => {
            let case_id = args
                .case_id
                .unwrap_or_else(|| format!("case_{}", &Uuid::new_v4().simple().to_string()[..12]));
            match store.get_case(&case_id) {
                Ok(Some(_)) => {
                    eprintln!("case already exists: {case_id}");
                    1
                }
                Ok(None) => {
                    let case = Case {
                        case_id,
                        title: args.title,
                        status: CaseStatus::Started,
                        user_id: args.user_id,
                        agent_id: args.agent_id,
                        started_at: Utc::now(),
                        ended_at: None,
                        final_summary: None,
                    };
                    match store.create_case(&case) {
                        Ok(()) => render(&case, config.format.value),
                        Err(error) => {
                            eprintln!("{error}");
                            1
                        }
                    }
                }
                Err(error) => {
                    eprintln!("{error}");
                    1
                }
            }
        }
        CaseSubcommand::List => match store.list_cases() {
            Ok(cases) => render_case_list(&cases, config.format.value),
            Err(error) => {
                eprintln!("{error}");
                1
            }
        },
        CaseSubcommand::Show(args) => match store.get_case(&args.case_id) {
            Ok(Some(case)) => render(&case, config.format.value),
            Ok(None) => {
                eprintln!("case not found: {}", args.case_id);
                1
            }
            Err(error) => {
                eprintln!("{error}");
                1
            }
        },
    }
}

fn handle_event(command: EventCommand, config: &ResolvedRuntimeConfig) -> i32 {
    let store = match SqliteStore::new(&config.db.path) {
        Ok(store) => store,
        Err(error) => {
            eprintln!("{error}");
            return 1;
        }
    };

    match command.command {
        EventSubcommand::Append(args) => {
            let payload = match serde_json::from_str::<Value>(&args.payload) {
                Ok(Value::Object(payload)) => payload,
                Ok(_) => {
                    eprintln!("event payload must be a JSON object");
                    return 1;
                }
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };

            let event_type = match args.event_type.parse::<EventType>() {
                Ok(value) => value,
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };
            let actor = match args.actor.parse::<EventActor>() {
                Ok(value) => value,
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };

            if let Some(code) = ensure_case_exists(&store, &args.case_id) {
                return code;
            }

            let event = Event {
                event_id: args.event_id.unwrap_or_else(|| {
                    format!("evt_{}", &Uuid::new_v4().simple().to_string()[..12])
                }),
                case_id: args.case_id.clone(),
                event_type,
                actor,
                timestamp: Utc::now(),
                sequence_no: match store.next_event_sequence(&args.case_id) {
                    Ok(sequence_no) => sequence_no,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                },
                parent_event_id: None,
                payload: Value::Object(payload),
            };

            match store.append_event(&event) {
                Ok(()) => render(&event, config.format.value),
                Err(error) => {
                    eprintln!("{error}");
                    1
                }
            }
        }
        EventSubcommand::ImportJsonl(args) => {
            let file = match File::open(&args.path) {
                Ok(file) => file,
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };

            let mut imported = Vec::new();
            for (index, line_result) in BufReader::new(file).lines().enumerate() {
                let line_number = index + 1;
                let line = match line_result {
                    Ok(line) => line,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };
                let stripped = line.trim();
                if stripped.is_empty() {
                    continue;
                }

                let input = match serde_json::from_str::<ImportedEventRecord>(stripped) {
                    Ok(input) => input,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };

                let case_id = match input.case_id.clone().or_else(|| args.case_id.clone()) {
                    Some(case_id) if !case_id.is_empty() => case_id,
                    _ => {
                        eprintln!("line {line_number}: case_id is required");
                        return 1;
                    }
                };

                if let Some(code) = ensure_case_exists(&store, &case_id) {
                    return code;
                }

                let event = match imported_event_to_event(input, &store, &case_id) {
                    Ok(event) => event,
                    Err(error) => {
                        eprintln!("line {line_number}: {error}");
                        return 1;
                    }
                };

                match store.append_event(&event) {
                    Ok(()) => imported.push(event),
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                }
            }

            render_event_list(&imported, config.format.value)
        }
    }
}

fn handle_decision(command: DecisionCommand, config: &ResolvedRuntimeConfig) -> i32 {
    let store = match SqliteStore::new(&config.db.path) {
        Ok(store) => store,
        Err(error) => {
            eprintln!("{error}");
            return 1;
        }
    };

    match command.command {
        DecisionSubcommand::Extract(args) => {
            if let Some(code) = ensure_case_exists(&store, &args.case_id) {
                return code;
            }

            let events = match store.list_events(&args.case_id) {
                Ok(events) => events,
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };
            let decisions = extract_decisions(&args.case_id, &events);
            if let Err(error) = store.replace_decisions(&args.case_id, &decisions) {
                eprintln!("{error}");
                return 1;
            }
            render_decision_list(&decisions, config.format.value)
        }
        DecisionSubcommand::List(args) => {
            if let Some(code) = ensure_case_exists(&store, &args.case_id) {
                return code;
            }

            match store.list_decisions(&args.case_id) {
                Ok(decisions) => render_decision_list(&decisions, config.format.value),
                Err(error) => {
                    eprintln!("{error}");
                    1
                }
            }
        }
    }
}

fn handle_replay(command: ReplayCommand, config: &ResolvedRuntimeConfig) -> i32 {
    let store = match SqliteStore::new(&config.db.path) {
        Ok(store) => store,
        Err(error) => {
            eprintln!("{error}");
            return 1;
        }
    };

    match command.command {
        ReplaySubcommand::Case(args) => {
            let case = match store.get_case(&args.case_id) {
                Ok(Some(case)) => case,
                Ok(None) => {
                    eprintln!("case not found: {}", args.case_id);
                    return 1;
                }
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };
            let events = match store.list_events(&args.case_id) {
                Ok(events) => events,
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };
            let decisions = match store.list_decisions(&args.case_id) {
                Ok(decisions) => decisions,
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };
            let artifacts = match derive_artifacts(&store, &args.case_id, &events) {
                Ok(artifacts) => artifacts,
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };
            let summary = case
                .final_summary
                .clone()
                .or_else(|| Some(build_case_summary(&case, &events, &decisions)));
            let replay = ReplayResponse {
                case,
                events,
                decisions,
                artifacts,
                summary,
            };
            render_replay_response(&replay, config.format.value)
        }
    }
}

fn handle_precedent(command: PrecedentCommand, config: &ResolvedRuntimeConfig) -> i32 {
    let store = match SqliteStore::new(&config.db.path) {
        Ok(store) => store,
        Err(error) => {
            eprintln!("{error}");
            return 1;
        }
    };

    match command.command {
        PrecedentSubcommand::Find(args) => {
            let current_case = match store.get_case(&args.case_id) {
                Ok(Some(case)) => case,
                Ok(None) => {
                    eprintln!("case not found: {}", args.case_id);
                    return 1;
                }
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };
            let current_events = match store.list_events(&args.case_id) {
                Ok(events) => events,
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };
            let current_decisions = match store.list_decisions(&args.case_id) {
                Ok(decisions) => decisions,
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };
            let current_fingerprint =
                build_case_fingerprint(&current_case, &current_events, &current_decisions);

            let mut candidates: Vec<(i64, Precedent)> = Vec::new();
            let cases = match store.list_cases() {
                Ok(cases) => cases,
                Err(error) => {
                    eprintln!("{error}");
                    return 1;
                }
            };
            for other_case in cases {
                if other_case.case_id == args.case_id {
                    continue;
                }
                let other_events = match store.list_events(&other_case.case_id) {
                    Ok(events) => events,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };
                let other_decisions = match store.list_decisions(&other_case.case_id) {
                    Ok(decisions) => decisions,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };
                let other_fingerprint =
                    build_case_fingerprint(&other_case, &other_events, &other_decisions);
                let (score, similarities, differences) =
                    compare_fingerprints(&current_fingerprint, &other_fingerprint);
                if score <= 0 {
                    continue;
                }
                candidates.push((
                    score,
                    Precedent {
                        case_id: other_case.case_id.clone(),
                        title: other_case.title.clone(),
                        summary: build_case_summary(&other_case, &other_events, &other_decisions),
                        similarity_score: score,
                        similarities,
                        differences,
                        reusable_takeaway: build_reusable_takeaway(&other_case, &other_decisions),
                        historical_outcome: other_case.final_summary.clone(),
                    },
                ));
            }

            candidates.sort_by(|left, right| {
                right
                    .0
                    .cmp(&left.0)
                    .then_with(|| left.1.case_id.cmp(&right.1.case_id))
            });
            let precedents = candidates
                .into_iter()
                .take(args.limit)
                .map(|(_, precedent)| precedent)
                .collect::<Vec<_>>();
            render_precedent_list(&precedents, config.format.value)
        }
    }
}

fn handle_capture(command: CaptureCommand, config: &ResolvedRuntimeConfig) -> i32 {
    match command.runtime {
        CaptureRuntime::Openclaw(command) => match command.command {
            OpenclawCaptureSubcommand::ListSessions(args) => {
                let sessions_root = args
                    .sessions_root
                    .unwrap_or_else(capture_openclaw::default_sessions_root);
                match capture_openclaw::list_sessions(&sessions_root, args.limit) {
                    Ok(sessions) => match config.format.value {
                        OutputFormat::Json => match serde_json::to_string_pretty(&sessions) {
                            Ok(json) => {
                                println!("{json}");
                                0
                            }
                            Err(error) => {
                                eprintln!("{error}");
                                1
                            }
                        },
                        OutputFormat::Text => {
                            for session in sessions {
                                println!(
                                    "{} {} {}",
                                    session.session_id,
                                    session
                                        .updated_at
                                        .map(|value| value.to_rfc3339())
                                        .unwrap_or_else(|| "<unknown>".to_string()),
                                    session.transcript_path
                                );
                            }
                            0
                        }
                    },
                    Err(error) => {
                        eprintln!("{error}");
                        1
                    }
                }
            }
            OpenclawCaptureSubcommand::ImportSession(args) => {
                let store = match SqliteStore::new(&config.db.path) {
                    Ok(store) => store,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };

                let (transcript_path, session_title) = match resolve_openclaw_session_target(&args)
                {
                    Ok(target) => target,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };

                let import_result = match import_openclaw_session(
                    &store,
                    &transcript_path,
                    &args.case_id,
                    args.title.as_deref().unwrap_or(&session_title),
                    args.user_id.as_deref(),
                    Some(args.agent_id.as_str()),
                ) {
                    Ok(result) => result,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };

                match serde_json::to_string_pretty(&import_result) {
                    Ok(json) => {
                        println!("{json}");
                        0
                    }
                    Err(error) => {
                        eprintln!("{error}");
                        1
                    }
                }
            }
            OpenclawCaptureSubcommand::CollectSessions(args) => {
                let store = match SqliteStore::new(&config.db.path) {
                    Ok(store) => store,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };
                let sessions_root = args
                    .sessions_root
                    .unwrap_or_else(capture_openclaw::default_sessions_root);
                let state_path = args
                    .state_file
                    .unwrap_or_else(|| config.state_file.path.clone());
                let references = match capture_openclaw::list_sessions(&sessions_root, 200) {
                    Ok(references) => references,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };
                let mut state = match capture_openclaw::load_collection_state(&state_path) {
                    Ok(state) => state,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };
                let mut seen = state
                    .imported_session_ids
                    .iter()
                    .cloned()
                    .collect::<HashSet<_>>();
                let mut imported = Vec::new();
                let mut skipped = Vec::new();

                for reference in references {
                    if seen.contains(&reference.session_id) {
                        skipped.push(reference.session_id.clone());
                        continue;
                    }
                    let import_result = match import_openclaw_session(
                        &store,
                        std::path::Path::new(&reference.transcript_path),
                        &capture_openclaw::case_id_for_session(&reference.session_id),
                        reference
                            .label
                            .as_deref()
                            .unwrap_or(&format!("OpenClaw session {}", reference.session_id)),
                        args.user_id.as_deref(),
                        Some(args.agent_id.as_str()),
                    ) {
                        Ok(result) => result,
                        Err(error) => {
                            eprintln!("{error}");
                            return 1;
                        }
                    };
                    imported.push(capture_openclaw::CollectedSessionResult {
                        session_id: reference.session_id.clone(),
                        transcript_path: reference.transcript_path.clone(),
                        case_id: import_result.case.case_id.clone(),
                        title: import_result.case.title.clone(),
                        imported_event_count: import_result.imported_event_count,
                        unsupported_record_type_counts: import_result
                            .unsupported_record_type_counts
                            .clone(),
                    });
                    seen.insert(reference.session_id.clone());
                    state.imported_session_ids.push(reference.session_id);
                    if imported.len() >= args.limit {
                        break;
                    }
                }

                if let Err(error) = capture_openclaw::write_collection_state(&state_path, &state) {
                    eprintln!("{error}");
                    return 1;
                }

                let result = capture_openclaw::OpenClawCollectionResult {
                    imported,
                    skipped_session_ids: skipped,
                    state_path: state_path.display().to_string(),
                };
                match serde_json::to_string_pretty(&result) {
                    Ok(json) => {
                        println!("{json}");
                        0
                    }
                    Err(error) => {
                        eprintln!("{error}");
                        1
                    }
                }
            }
            OpenclawCaptureSubcommand::ImportJsonl(args) => {
                let store = match SqliteStore::new(&config.db.path) {
                    Ok(store) => store,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };

                let case = match ensure_case(
                    &store,
                    &args.case_id,
                    &args.title,
                    args.user_id.as_deref(),
                    Some(args.agent_id.as_str()),
                ) {
                    Ok(case) => case,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };

                let file = match File::open(&args.path) {
                    Ok(file) => file,
                    Err(error) => {
                        eprintln!("{error}");
                        return 1;
                    }
                };
                let mut imported = Vec::new();
                for (index, line_result) in BufReader::new(file).lines().enumerate() {
                    let line_number = index + 1;
                    let line = match line_result {
                        Ok(line) => line,
                        Err(error) => {
                            eprintln!("{error}");
                            return 1;
                        }
                    };
                    let stripped = line.trim();
                    if stripped.is_empty() {
                        continue;
                    }
                    let raw_item = match serde_json::from_str::<Value>(stripped) {
                        Ok(Value::Object(item)) => item,
                        Ok(_) => {
                            eprintln!(
                                "line {line_number}: openclaw trace line must be a JSON object"
                            );
                            return 1;
                        }
                        Err(error) => {
                            eprintln!("{error}");
                            return 1;
                        }
                    };

                    let event = match normalize_openclaw_trace_line(
                        raw_item,
                        line_number,
                        &store,
                        &args.case_id,
                    ) {
                        Ok(event) => event,
                        Err(error) => {
                            eprintln!("{error}");
                            return 1;
                        }
                    };

                    match store.append_event(&event) {
                        Ok(()) => imported.push(event),
                        Err(error) => {
                            eprintln!("{error}");
                            return 1;
                        }
                    }
                }

                let output = CaptureImportOutput {
                    case,
                    imported_event_count: imported.len(),
                    events: imported,
                };
                match serde_json::to_string_pretty(&output) {
                    Ok(json) => {
                        println!("{json}");
                        0
                    }
                    Err(error) => {
                        eprintln!("{error}");
                        1
                    }
                }
            }
        },
        CaptureRuntime::Codex(command) => {
            render_not_implemented_path(capture_path(CaptureCommand {
                runtime: CaptureRuntime::Codex(command),
            }))
        }
    }
}

fn render_not_implemented_path(path: Vec<&'static str>) -> i32 {
    let error = not_implemented(&path);
    eprintln!("{error}");
    1
}

fn render<T>(payload: &T, format: OutputFormat) -> i32
where
    T: Serialize + TextRenderable,
{
    match format {
        OutputFormat::Json => match serde_json::to_string_pretty(payload) {
            Ok(json) => {
                println!("{json}");
                0
            }
            Err(error) => {
                eprintln!("{error}");
                1
            }
        },
        OutputFormat::Text => {
            println!("{}", payload.render_text());
            0
        }
    }
}

fn render_case_list(cases: &[Case], format: OutputFormat) -> i32 {
    match format {
        OutputFormat::Json => match serde_json::to_string_pretty(cases) {
            Ok(json) => {
                println!("{json}");
                0
            }
            Err(error) => {
                eprintln!("{error}");
                1
            }
        },
        OutputFormat::Text => {
            for case in cases {
                println!("{} {} {}", case.case_id, case.status, case.title);
            }
            0
        }
    }
}

fn render_event_list(events: &[Event], format: OutputFormat) -> i32 {
    match format {
        OutputFormat::Json => match serde_json::to_string_pretty(events) {
            Ok(json) => {
                println!("{json}");
                0
            }
            Err(error) => {
                eprintln!("{error}");
                1
            }
        },
        OutputFormat::Text => {
            for event in events {
                println!(
                    "[{}] {} {} {}",
                    event.sequence_no, event.event_id, event.event_type, event.actor
                );
            }
            0
        }
    }
}

fn render_decision_list(decisions: &[Decision], format: OutputFormat) -> i32 {
    match format {
        OutputFormat::Json => match serde_json::to_string_pretty(decisions) {
            Ok(json) => {
                println!("{json}");
                0
            }
            Err(error) => {
                eprintln!("{error}");
                1
            }
        },
        OutputFormat::Text => {
            for (index, decision) in decisions.iter().enumerate() {
                if index > 0 {
                    println!();
                }
                println!("{}", decision.render_text());
            }
            0
        }
    }
}

fn render_replay_response(replay: &ReplayResponse, format: OutputFormat) -> i32 {
    match format {
        OutputFormat::Json => match serde_json::to_string_pretty(replay) {
            Ok(json) => {
                println!("{json}");
                0
            }
            Err(error) => {
                eprintln!("{error}");
                1
            }
        },
        OutputFormat::Text => {
            println!("{}", replay.render_text());
            0
        }
    }
}

fn render_precedent_list(precedents: &[Precedent], format: OutputFormat) -> i32 {
    match format {
        OutputFormat::Json => match serde_json::to_string_pretty(precedents) {
            Ok(json) => {
                println!("{json}");
                0
            }
            Err(error) => {
                eprintln!("{error}");
                1
            }
        },
        OutputFormat::Text => {
            for precedent in precedents {
                println!("{}", precedent.render_text());
            }
            0
        }
    }
}

trait TextRenderable {
    fn render_text(&self) -> String;
}

impl TextRenderable for Case {
    fn render_text(&self) -> String {
        let mut lines = vec![
            format!("case_id: {}", self.case_id),
            format!("title: {}", self.title),
            format!("status: {}", self.status),
            format!("started_at: {}", self.started_at.to_rfc3339()),
        ];
        if let Some(user_id) = &self.user_id {
            lines.push(format!("user_id: {user_id}"));
        }
        if let Some(agent_id) = &self.agent_id {
            lines.push(format!("agent_id: {agent_id}"));
        }
        if let Some(ended_at) = &self.ended_at {
            lines.push(format!("ended_at: {}", ended_at.to_rfc3339()));
        }
        if let Some(summary) = &self.final_summary {
            lines.push(format!("final_summary: {summary}"));
        }
        lines.join("\n")
    }
}

impl TextRenderable for Event {
    fn render_text(&self) -> String {
        let mut lines = vec![
            format!("event_id: {}", self.event_id),
            format!("case_id: {}", self.case_id),
            format!("event_type: {}", self.event_type),
            format!("actor: {}", self.actor),
            format!("timestamp: {}", self.timestamp.to_rfc3339()),
            format!("sequence_no: {}", self.sequence_no),
            format!("payload: {}", self.payload),
        ];
        if let Some(parent_event_id) = &self.parent_event_id {
            lines.push(format!("parent_event_id: {parent_event_id}"));
        }
        lines.join("\n")
    }
}

impl TextRenderable for Decision {
    fn render_text(&self) -> String {
        let mut lines = vec![
            format!(
                "[{}] {}: {}",
                self.sequence_no, self.decision_type, self.title
            ),
            format!("  question: {}", self.question),
            format!("  chosen_action: {}", self.chosen_action),
            format!("  confidence: {:.2}", self.confidence),
            format!("  goal: {}", self.explanation.goal),
            format!("  why: {}", self.explanation.selection_reason),
        ];
        if !self.explanation.evidence.is_empty() {
            lines.push(format!(
                "  evidence: {}",
                self.explanation.evidence.join(", ")
            ));
        }
        if !self.explanation.constraints.is_empty() {
            lines.push(format!(
                "  constraints: {}",
                self.explanation.constraints.join(", ")
            ));
        }
        if let Some(result) = &self.explanation.result {
            lines.push(format!("  result: {result}"));
        }
        lines.join("\n")
    }
}

impl TextRenderable for Artifact {
    fn render_text(&self) -> String {
        let mut lines = vec![format!("- {}: {}", self.artifact_type, self.uri_or_path)];
        if let Some(summary) = &self.summary {
            lines.push(format!("    summary: {summary}"));
        }
        lines.join("\n")
    }
}

impl TextRenderable for ReplayResponse {
    fn render_text(&self) -> String {
        let mut lines = vec![
            format!("Case {}: {}", self.case.case_id, self.case.title),
            format!("Status: {}", self.case.status),
            "Events:".to_string(),
        ];
        for event in &self.events {
            lines.push(format!(
                "  [{}] {} ({})",
                event.sequence_no, event.event_type, event.actor
            ));
        }
        lines.push("Decisions:".to_string());
        for decision in &self.decisions {
            lines.push(format!(
                "  [{}] {}: {}",
                decision.sequence_no, decision.decision_type, decision.title
            ));
            lines.push(format!(
                "      why: {}",
                decision.explanation.selection_reason
            ));
            if let Some(result) = &decision.explanation.result {
                lines.push(format!("      result: {result}"));
            }
        }
        lines.push("Artifacts:".to_string());
        for artifact in &self.artifacts {
            lines.push(format!(
                "  - {}: {}",
                artifact.artifact_type, artifact.uri_or_path
            ));
            if let Some(summary) = &artifact.summary {
                lines.push(format!("      summary: {summary}"));
            }
        }
        if let Some(summary) = &self.summary {
            lines.push(format!("Summary: {summary}"));
        }
        lines.join("\n")
    }
}

impl TextRenderable for Precedent {
    fn render_text(&self) -> String {
        let mut lines = vec![
            format!(
                "{} (score={}): {}",
                self.case_id, self.similarity_score, self.title
            ),
            format!("  summary: {}", self.summary),
        ];
        if !self.similarities.is_empty() {
            lines.push(format!("  similarities: {}", self.similarities.join(", ")));
        }
        if !self.differences.is_empty() {
            lines.push(format!("  differences: {}", self.differences.join(", ")));
        }
        if let Some(takeaway) = &self.reusable_takeaway {
            lines.push(format!("  reusable_takeaway: {takeaway}"));
        }
        if let Some(outcome) = &self.historical_outcome {
            lines.push(format!("  historical_outcome: {outcome}"));
        }
        lines.join("\n")
    }
}

impl TextRenderable for VersionReport {
    fn render_text(&self) -> String {
        format!("{} {} ({})", self.name, self.version, self.contract_phase)
    }
}

impl TextRenderable for PathsDoctorReport {
    fn render_text(&self) -> String {
        let mut lines = Vec::new();
        if let Some(config_file) = &self.config_file {
            lines.push(format!(
                "config_file: {} (exists: {})",
                config_file.path.display(),
                config_file.exists
            ));
        } else {
            lines.push("config_file: <none>".to_string());
        }
        lines.push(render_path_line("home", &self.home));
        lines.push(render_path_line("db", &self.db));
        lines.push(render_path_line("invocation_log", &self.invocation_log));
        lines.push(render_path_line("state_file", &self.state_file));
        lines.join("\n")
    }
}

impl TextRenderable for StorageDoctorReport {
    fn render_text(&self) -> String {
        [
            render_storage_line("db", &self.db),
            render_storage_line("invocation_log", &self.invocation_log),
            render_storage_line("state_file", &self.state_file),
        ]
        .join("\n")
    }
}

impl TextRenderable for openprecedent_contracts::EnvironmentDoctorReport {
    fn render_text(&self) -> String {
        let mut lines = vec![
            format!("format: {} ({:?})", self.format.value, self.format.source),
            format!(
                "no_color: {} ({:?})",
                self.no_color.value, self.no_color.source
            ),
        ];
        if let Some(config_file) = &self.config_file {
            lines.push(format!("config_file: {}", config_file.path.display()));
        } else {
            lines.push("config_file: <none>".to_string());
        }
        for variable in &self.variables {
            let value = variable.value.as_deref().unwrap_or("<unset>");
            lines.push(format!("{}: {}", variable.name, value));
        }
        lines.join("\n")
    }
}

fn render_path_line(label: &str, path: &openprecedent_contracts::ResolvedPath) -> String {
    let mut line = format!("{label}: {} ({:?})", path.path.display(), path.source);
    if let Some(derived_from) = path.derived_from {
        line.push_str(&format!(" derived_from={derived_from}"));
    }
    line
}

fn render_storage_line(label: &str, path: &openprecedent_contracts::StoragePathReport) -> String {
    format!(
        "{label}: {} ({:?}) exists={} parent_exists={}",
        path.path.display(),
        path.source,
        path.exists,
        path.parent_exists
    )
}

fn ensure_case_exists(store: &SqliteStore, case_id: &str) -> Option<i32> {
    match store.get_case(case_id) {
        Ok(Some(_)) => None,
        Ok(None) => {
            eprintln!("case not found: {case_id}");
            Some(1)
        }
        Err(error) => {
            eprintln!("{error}");
            Some(1)
        }
    }
}

fn ensure_case(
    store: &SqliteStore,
    case_id: &str,
    title: &str,
    user_id: Option<&str>,
    agent_id: Option<&str>,
) -> Result<Case, String> {
    match store.get_case(case_id).map_err(|error| error.to_string())? {
        Some(case) => Ok(case),
        None => {
            let case = Case {
                case_id: case_id.to_string(),
                title: title.to_string(),
                status: CaseStatus::Started,
                user_id: user_id.map(ToString::to_string),
                agent_id: agent_id.map(ToString::to_string),
                started_at: Utc::now(),
                ended_at: None,
                final_summary: None,
            };
            store
                .create_case(&case)
                .map_err(|error| error.to_string())?;
            Ok(case)
        }
    }
}

fn resolve_openclaw_session_target(
    args: &OpenClawImportSessionArgs,
) -> Result<(std::path::PathBuf, String), String> {
    if let Some(session_file) = &args.session_file {
        let title = args.title.clone().unwrap_or_else(|| {
            session_file
                .file_stem()
                .and_then(|item| item.to_str())
                .unwrap_or("openclaw-session")
                .to_string()
        });
        return Ok((session_file.clone(), title));
    }

    let sessions_root = args
        .sessions_root
        .clone()
        .unwrap_or_else(capture_openclaw::default_sessions_root);
    let sessions =
        capture_openclaw::list_sessions(&sessions_root, 50).map_err(|error| error.to_string())?;
    if args.latest {
        let session = sessions
            .first()
            .ok_or_else(|| "no OpenClaw sessions found".to_string())?;
        return Ok((
            std::path::PathBuf::from(&session.transcript_path),
            args.title
                .clone()
                .or_else(|| session.label.clone())
                .unwrap_or_else(|| session.session_id.clone()),
        ));
    }
    if let Some(session_id) = &args.session_id {
        for session in sessions {
            if &session.session_id == session_id {
                return Ok((
                    std::path::PathBuf::from(&session.transcript_path),
                    args.title
                        .clone()
                        .or_else(|| session.label.clone())
                        .unwrap_or_else(|| session.session_id.clone()),
                ));
            }
        }
        return Err(format!("OpenClaw session not found: {session_id}"));
    }

    Err("one of --session-file, --session-id, or --latest is required".to_string())
}

fn import_openclaw_session(
    store: &SqliteStore,
    transcript_path: &std::path::Path,
    case_id: &str,
    title: &str,
    user_id: Option<&str>,
    agent_id: Option<&str>,
) -> Result<OpenClawSessionImportOutput, String> {
    let file = File::open(transcript_path).map_err(|error| error.to_string())?;
    let mut normalized_imports = Vec::new();
    let mut unsupported = std::collections::BTreeMap::<String, usize>::new();

    for (index, line_result) in BufReader::new(file).lines().enumerate() {
        let line_number = index + 1;
        let line = line_result.map_err(|error| error.to_string())?;
        let stripped = line.trim();
        if stripped.is_empty() {
            continue;
        }
        let raw_item = match serde_json::from_str::<Value>(stripped) {
            Ok(Value::Object(item)) => item,
            Ok(_) => {
                return Err(format!(
                    "line {line_number}: openclaw session line must be a JSON object"
                ))
            }
            Err(error) => return Err(error.to_string()),
        };
        let (events, unsupported_type) =
            normalize_openclaw_session_line(raw_item, line_number, transcript_path)?;
        if let Some(unsupported_type) = unsupported_type {
            *unsupported.entry(unsupported_type).or_insert(0) += 1;
        }
        normalized_imports.extend(events);
    }

    let session_id = openclaw_session_id_from_import(&normalized_imports, transcript_path);
    if let Some(existing_case_id) = store
        .find_case_id_by_openclaw_session_id(&session_id)
        .map_err(|error| error.to_string())?
    {
        let existing_case = store
            .get_case(&existing_case_id)
            .map_err(|error| error.to_string())?
            .ok_or_else(|| format!("case not found: {existing_case_id}"))?;
        return Ok(OpenClawSessionImportOutput {
            case: existing_case,
            transcript_path: transcript_path.display().to_string(),
            imported_event_count: 0,
            unsupported_record_type_counts: unsupported,
            events: Vec::new(),
        });
    }

    let case = ensure_case(store, case_id, title, user_id, agent_id)?;
    let mut imported = Vec::new();
    for mut event in normalized_imports {
        event.case_id = case_id.to_string();
        event.sequence_no = store
            .next_event_sequence(case_id)
            .map_err(|error| error.to_string())?;
        store
            .append_event(&event)
            .map_err(|error| error.to_string())?;
        imported.push(event);
    }

    Ok(OpenClawSessionImportOutput {
        case,
        transcript_path: transcript_path.display().to_string(),
        imported_event_count: imported.len(),
        unsupported_record_type_counts: unsupported,
        events: imported,
    })
}

#[derive(Debug, Deserialize)]
struct ImportedEventRecord {
    case_id: Option<String>,
    event_id: Option<String>,
    event_type: String,
    actor: String,
    timestamp: Option<String>,
    parent_event_id: Option<String>,
    sequence_no: Option<i64>,
    #[serde(default)]
    payload: Value,
}

fn imported_event_to_event(
    input: ImportedEventRecord,
    store: &SqliteStore,
    case_id: &str,
) -> Result<Event, String> {
    let ImportedEventRecord {
        case_id: _,
        event_id,
        event_type,
        actor,
        timestamp,
        parent_event_id,
        sequence_no,
        payload,
    } = input;

    let event_type = event_type
        .parse::<EventType>()
        .map_err(|error| error.to_string())?;
    let actor = actor
        .parse::<EventActor>()
        .map_err(|error| error.to_string())?;
    let timestamp = match timestamp {
        Some(value) => DateTime::parse_from_rfc3339(&value)
            .map(|value| value.with_timezone(&Utc))
            .map_err(|error| error.to_string())?,
        None => Utc::now(),
    };
    let payload = match payload {
        Value::Object(payload) => Value::Object(payload),
        Value::Null => Value::Object(Map::new()),
        _ => return Err("payload must be a JSON object".to_string()),
    };
    let sequence_no = match sequence_no {
        Some(sequence_no) => sequence_no,
        None => store
            .next_event_sequence(case_id)
            .map_err(|error| error.to_string())?,
    };

    Ok(Event {
        event_id: event_id
            .unwrap_or_else(|| format!("evt_{}", &Uuid::new_v4().simple().to_string()[..12])),
        case_id: case_id.to_string(),
        event_type,
        actor,
        timestamp,
        sequence_no,
        parent_event_id,
        payload,
    })
}

fn normalize_openclaw_trace_line(
    raw_item: serde_json::Map<String, Value>,
    line_no: usize,
    store: &SqliteStore,
    case_id: &str,
) -> Result<Event, String> {
    let kind = raw_item
        .get("kind")
        .and_then(string_or_none)
        .ok_or_else(|| format!("line {line_no}: kind is required for openclaw import"))?;
    let timestamp = parse_optional_timestamp(raw_item.get("timestamp"))
        .map_err(|error| format!("line {line_no}: {error}"))?
        .unwrap_or_else(Utc::now);
    let event_id = raw_item.get("event_id").and_then(string_or_none);

    let (event_type, actor, payload) = match kind.as_str() {
        "user_message" => (
            EventType::MessageUser,
            EventActor::User,
            json_object([
                (
                    "message",
                    raw_item
                        .get("content")
                        .and_then(string_or_none)
                        .unwrap_or_default()
                        .into(),
                ),
                ("source", "openclaw".into()),
            ]),
        ),
        "agent_message" => (
            EventType::MessageAgent,
            EventActor::Agent,
            json_object([
                (
                    "message",
                    raw_item
                        .get("content")
                        .and_then(string_or_none)
                        .unwrap_or_default()
                        .into(),
                ),
                ("source", "openclaw".into()),
            ]),
        ),
        "tool_call" => (
            EventType::ToolCalled,
            EventActor::Agent,
            json_object([
                (
                    "tool_name",
                    raw_item
                        .get("tool_name")
                        .and_then(string_or_none)
                        .unwrap_or_else(|| "unknown_tool".to_string())
                        .into(),
                ),
                (
                    "reason",
                    raw_item
                        .get("reason")
                        .and_then(string_or_none)
                        .map(Value::String)
                        .unwrap_or(Value::Null),
                ),
                (
                    "arguments",
                    raw_item
                        .get("arguments")
                        .cloned()
                        .filter(|value| value.is_object())
                        .unwrap_or_else(|| Value::Object(Map::new())),
                ),
                ("source", "openclaw".into()),
            ]),
        ),
        "tool_result" => (EventType::ToolCompleted, EventActor::Tool, {
            let mut payload = raw_item.clone();
            payload.remove("kind");
            payload.remove("timestamp");
            payload.remove("event_id");
            Value::Object(payload)
        }),
        "command" => (
            EventType::CommandCompleted,
            EventActor::System,
            json_object([
                (
                    "command",
                    raw_item
                        .get("command")
                        .and_then(string_or_none)
                        .unwrap_or_default()
                        .into(),
                ),
                (
                    "exit_code",
                    raw_item
                        .get("exit_code")
                        .and_then(|value| value.as_i64())
                        .unwrap_or(0)
                        .into(),
                ),
                (
                    "stdout",
                    raw_item
                        .get("stdout")
                        .and_then(string_or_none)
                        .map(Value::String)
                        .unwrap_or(Value::Null),
                ),
                (
                    "stderr",
                    raw_item
                        .get("stderr")
                        .and_then(string_or_none)
                        .map(Value::String)
                        .unwrap_or(Value::Null),
                ),
                ("source", "openclaw".into()),
            ]),
        ),
        "file_write" => (
            EventType::FileWrite,
            EventActor::Agent,
            json_object([
                (
                    "path",
                    raw_item
                        .get("path")
                        .and_then(string_or_none)
                        .unwrap_or_else(|| "unknown_path".to_string())
                        .into(),
                ),
                (
                    "summary",
                    raw_item
                        .get("summary")
                        .and_then(string_or_none)
                        .map(Value::String)
                        .unwrap_or(Value::Null),
                ),
                ("source", "openclaw".into()),
            ]),
        ),
        "confirmation" => (
            EventType::UserConfirmed,
            EventActor::User,
            json_object([
                (
                    "message",
                    raw_item
                        .get("content")
                        .and_then(string_or_none)
                        .unwrap_or_default()
                        .into(),
                ),
                ("source", "openclaw".into()),
            ]),
        ),
        "completed" => (
            EventType::CaseCompleted,
            EventActor::System,
            json_object([
                (
                    "summary",
                    raw_item
                        .get("summary")
                        .and_then(string_or_none)
                        .unwrap_or_else(|| "OpenClaw task completed".to_string())
                        .into(),
                ),
                ("source", "openclaw".into()),
            ]),
        ),
        "failed" => (
            EventType::CaseFailed,
            EventActor::System,
            json_object([
                (
                    "summary",
                    raw_item
                        .get("summary")
                        .and_then(string_or_none)
                        .unwrap_or_else(|| "OpenClaw task failed".to_string())
                        .into(),
                ),
                ("source", "openclaw".into()),
            ]),
        ),
        _ => {
            return Err(format!(
                "line {line_no}: unsupported openclaw kind '{kind}'"
            ))
        }
    };

    Ok(Event {
        event_id: event_id
            .unwrap_or_else(|| format!("evt_{}", &Uuid::new_v4().simple().to_string()[..12])),
        case_id: case_id.to_string(),
        event_type,
        actor,
        timestamp,
        sequence_no: store
            .next_event_sequence(case_id)
            .map_err(|error| error.to_string())?,
        parent_event_id: None,
        payload,
    })
}

fn normalize_openclaw_session_line(
    raw_item: serde_json::Map<String, Value>,
    line_no: usize,
    transcript_path: &std::path::Path,
) -> Result<(Vec<Event>, Option<String>), String> {
    let record_type = raw_item
        .get("type")
        .and_then(string_or_none)
        .ok_or_else(|| format!("line {line_no}: type is required for openclaw session import"))?;
    let timestamp = parse_optional_timestamp(raw_item.get("timestamp"))
        .map_err(|error| format!("line {line_no}: {error}"))?;
    let record_id = raw_item
        .get("id")
        .and_then(string_or_none)
        .unwrap_or_else(|| format!("session_line_{line_no}"));
    let parent_id = raw_item.get("parentId").and_then(string_or_none);

    match record_type.as_str() {
        "session" => Ok((
            vec![session_event(
                &format!("evt_session_{record_id}"),
                EventType::CaseStarted,
                EventActor::System,
                timestamp,
                parent_id,
                json_object([
                    (
                        "session_id",
                        raw_item
                            .get("id")
                            .and_then(string_or_none)
                            .unwrap_or_else(|| {
                                transcript_path
                                    .file_stem()
                                    .and_then(|item| item.to_str())
                                    .unwrap_or_default()
                                    .to_string()
                            })
                            .into(),
                    ),
                    (
                        "transcript_version",
                        raw_item.get("version").cloned().unwrap_or(Value::Null),
                    ),
                    (
                        "cwd",
                        raw_item
                            .get("cwd")
                            .and_then(string_or_none)
                            .map(Value::String)
                            .unwrap_or(Value::Null),
                    ),
                    ("source", "openclaw.session".into()),
                ]),
            )],
            None,
        )),
        "checkpoint" => Ok((
            vec![session_event(
                &format!("evt_checkpoint_{record_id}"),
                EventType::CheckpointSaved,
                EventActor::System,
                timestamp,
                parent_id,
                json_object([
                    (
                        "checkpoint_id",
                        raw_item
                            .get("id")
                            .and_then(string_or_none)
                            .unwrap_or_else(|| record_id.clone())
                            .into(),
                    ),
                    (
                        "status",
                        raw_item
                            .get("status")
                            .and_then(string_or_none)
                            .map(Value::String)
                            .unwrap_or(Value::Null),
                    ),
                    ("source", "openclaw.session".into()),
                ]),
            )],
            None,
        )),
        "model_change" => Ok((
            vec![session_event(
                &format!("evt_model_{record_id}"),
                EventType::ModelCompleted,
                EventActor::System,
                timestamp,
                parent_id,
                json_object([
                    (
                        "provider",
                        raw_item
                            .get("provider")
                            .and_then(string_or_none)
                            .map(Value::String)
                            .unwrap_or(Value::Null),
                    ),
                    (
                        "model_id",
                        raw_item
                            .get("modelId")
                            .and_then(string_or_none)
                            .map(Value::String)
                            .unwrap_or(Value::Null),
                    ),
                    ("source", "openclaw.session".into()),
                ]),
            )],
            None,
        )),
        "thinking_level_change" => Ok((
            vec![session_event(
                &format!("evt_thinking_level_{record_id}"),
                EventType::ModelInvoked,
                EventActor::System,
                timestamp,
                parent_id,
                json_object([
                    (
                        "thinking_level",
                        raw_item
                            .get("thinkingLevel")
                            .and_then(string_or_none)
                            .or_else(|| raw_item.get("level").and_then(string_or_none))
                            .map(Value::String)
                            .unwrap_or(Value::Null),
                    ),
                    (
                        "changed_by",
                        raw_item
                            .get("source")
                            .and_then(string_or_none)
                            .map(Value::String)
                            .unwrap_or(Value::Null),
                    ),
                    (
                        "trigger",
                        raw_item
                            .get("trigger")
                            .and_then(string_or_none)
                            .map(Value::String)
                            .unwrap_or(Value::Null),
                    ),
                    ("source", "openclaw.session".into()),
                ]),
            )],
            None,
        )),
        "custom" => {
            let custom =
                normalize_openclaw_custom_record(&raw_item, &record_id, parent_id, timestamp);
            match custom {
                Some(custom) => Ok((vec![custom], None)),
                None => Ok((Vec::new(), Some(record_type))),
            }
        }
        "message" => normalize_openclaw_message_record(raw_item, &record_id, parent_id, timestamp),
        _ => Ok((Vec::new(), Some(record_type))),
    }
}

fn session_event(
    event_id: &str,
    event_type: EventType,
    actor: EventActor,
    timestamp: Option<DateTime<Utc>>,
    parent_event_id: Option<String>,
    payload: Value,
) -> Event {
    Event {
        event_id: event_id.to_string(),
        case_id: String::new(),
        event_type,
        actor,
        timestamp: timestamp.unwrap_or_else(Utc::now),
        sequence_no: 0,
        parent_event_id,
        payload,
    }
}

fn normalize_openclaw_message_record(
    raw_item: serde_json::Map<String, Value>,
    record_id: &str,
    parent_id: Option<String>,
    timestamp: Option<DateTime<Utc>>,
) -> Result<(Vec<Event>, Option<String>), String> {
    let message = raw_item
        .get("message")
        .and_then(|value| value.as_object())
        .ok_or_else(|| "message record must contain an object message".to_string())?;
    let role = message.get("role").and_then(string_or_none);
    let content = message
        .get("content")
        .and_then(|value| value.as_array())
        .cloned()
        .unwrap_or_default();

    let mut normalized = Vec::new();
    match role.as_deref() {
        Some("user") => {
            let text = sanitize_openclaw_message_text(
                &extract_openclaw_text_segments(&content).join("\n"),
            );
            if let Some(text) = text {
                normalized.push(session_event(
                    &format!("evt_message_{record_id}"),
                    EventType::MessageUser,
                    EventActor::User,
                    timestamp,
                    parent_id,
                    json_object([
                        ("message", text.into()),
                        ("source", "openclaw.session".into()),
                    ]),
                ));
            }
            Ok((normalized, None))
        }
        Some("assistant") => {
            let visible_text = sanitize_openclaw_message_text(
                &extract_openclaw_visible_assistant_text(&content).join("\n"),
            );
            if let Some(text) = visible_text {
                normalized.push(session_event(
                    &format!("evt_message_{record_id}"),
                    EventType::MessageAgent,
                    EventActor::Agent,
                    timestamp,
                    parent_id.clone(),
                    json_object([
                        ("message", text.into()),
                        ("source", "openclaw.session".into()),
                    ]),
                ));
            }
            for (index, item) in content.iter().enumerate() {
                let Some(item) = item.as_object() else {
                    continue;
                };
                if item.get("type").and_then(string_or_none).as_deref() != Some("toolCall") {
                    continue;
                }
                let tool_name = item
                    .get("name")
                    .and_then(string_or_none)
                    .unwrap_or_else(|| "unknown_tool".to_string());
                let arguments = item
                    .get("arguments")
                    .cloned()
                    .filter(|value| value.is_object())
                    .unwrap_or_else(|| Value::Object(Map::new()));
                let tool_call_id = item.get("id").and_then(string_or_none);
                normalized.push(session_event(
                    &format!("evt_tool_{record_id}_{}", index + 1),
                    EventType::ToolCalled,
                    EventActor::Agent,
                    timestamp,
                    parent_id.clone(),
                    json_object([
                        ("tool_name", tool_name.clone().into()),
                        ("arguments", arguments.clone()),
                        (
                            "tool_call_id",
                            tool_call_id
                                .clone()
                                .map(Value::String)
                                .unwrap_or(Value::Null),
                        ),
                        ("source", "openclaw.session".into()),
                    ]),
                ));
                normalized.extend(normalize_openclaw_tool_call_events(
                    record_id,
                    index + 1,
                    parent_id.clone(),
                    timestamp,
                    &tool_name,
                    tool_call_id,
                    arguments,
                ));
            }
            Ok((normalized, None))
        }
        Some("toolResult") => {
            let text = extract_openclaw_text_segments(&content).join("\n");
            let text = if text.trim().is_empty() {
                None
            } else {
                Some(text)
            };
            let tool_name = message.get("toolName").and_then(string_or_none);
            let tool_call_id = message.get("toolCallId").and_then(string_or_none);
            let details = message
                .get("details")
                .cloned()
                .filter(|value| value.is_object())
                .unwrap_or_else(|| Value::Object(Map::new()));

            normalized.push(session_event(
                &format!("evt_tool_result_{record_id}"),
                EventType::ToolCompleted,
                EventActor::Tool,
                timestamp,
                parent_id.clone(),
                json_object([
                    (
                        "tool_name",
                        tool_name.clone().map(Value::String).unwrap_or(Value::Null),
                    ),
                    (
                        "tool_call_id",
                        tool_call_id
                            .clone()
                            .map(Value::String)
                            .unwrap_or(Value::Null),
                    ),
                    (
                        "content",
                        text.clone().map(Value::String).unwrap_or(Value::Null),
                    ),
                    (
                        "is_error",
                        message
                            .get("isError")
                            .and_then(|value| value.as_bool())
                            .unwrap_or(false)
                            .into(),
                    ),
                    ("details", details.clone()),
                    ("source", "openclaw.session".into()),
                ]),
            ));
            normalized.extend(normalize_openclaw_tool_result_events(
                record_id,
                parent_id,
                timestamp,
                tool_name,
                tool_call_id,
                text,
                details,
            ));
            Ok((normalized, None))
        }
        _ => Ok((Vec::new(), None)),
    }
}

fn normalize_openclaw_tool_call_events(
    record_id: &str,
    index: usize,
    parent_id: Option<String>,
    timestamp: Option<DateTime<Utc>>,
    tool_name: &str,
    tool_call_id: Option<String>,
    arguments: Value,
) -> Vec<Event> {
    let Some(arguments_obj) = arguments.as_object() else {
        return Vec::new();
    };

    if tool_name == "exec_command" {
        let Some(command) = arguments_obj.get("cmd").and_then(string_or_none) else {
            return Vec::new();
        };
        let mut events = vec![session_event(
            &format!("evt_command_started_{record_id}_{index}"),
            EventType::CommandStarted,
            EventActor::Agent,
            timestamp,
            parent_id.clone(),
            json_object([
                ("command", command.clone().into()),
                (
                    "tool_call_id",
                    tool_call_id
                        .clone()
                        .map(Value::String)
                        .unwrap_or(Value::Null),
                ),
                ("source", "openclaw.session".into()),
            ]),
        )];
        for (read_index, path) in extract_file_reads_from_command(&command)
            .into_iter()
            .enumerate()
        {
            events.push(session_event(
                &format!("evt_file_read_{record_id}_{index}_{}", read_index + 1),
                EventType::FileRead,
                EventActor::Agent,
                timestamp,
                parent_id.clone(),
                json_object([
                    ("path", path.into()),
                    ("command", command.clone().into()),
                    (
                        "tool_call_id",
                        tool_call_id
                            .clone()
                            .map(Value::String)
                            .unwrap_or(Value::Null),
                    ),
                    ("source", "openclaw.session".into()),
                ]),
            ));
        }
        return events;
    }

    if tool_name == "apply_patch" {
        let Some(patch_text) = arguments_obj.get("patch").and_then(string_or_none) else {
            return Vec::new();
        };
        return extract_paths_from_apply_patch(&patch_text)
            .into_iter()
            .enumerate()
            .map(|(path_index, path)| {
                session_event(
                    &format!("evt_file_write_{record_id}_{index}_{}", path_index + 1),
                    EventType::FileWrite,
                    EventActor::Agent,
                    timestamp,
                    parent_id.clone(),
                    json_object([
                        ("path", path.into()),
                        ("summary", "Modified via apply_patch".into()),
                        (
                            "tool_call_id",
                            tool_call_id
                                .clone()
                                .map(Value::String)
                                .unwrap_or(Value::Null),
                        ),
                        ("source", "openclaw.session".into()),
                    ]),
                )
            })
            .collect();
    }

    if tool_name == "view_image" {
        let Some(path) = arguments_obj.get("path").and_then(string_or_none) else {
            return Vec::new();
        };
        return vec![session_event(
            &format!("evt_file_read_{record_id}_{index}_image"),
            EventType::FileRead,
            EventActor::Agent,
            timestamp,
            parent_id,
            json_object([
                ("path", path.into()),
                (
                    "tool_call_id",
                    tool_call_id.map(Value::String).unwrap_or(Value::Null),
                ),
                ("source", "openclaw.session".into()),
            ]),
        )];
    }

    Vec::new()
}

fn normalize_openclaw_tool_result_events(
    record_id: &str,
    parent_id: Option<String>,
    timestamp: Option<DateTime<Utc>>,
    tool_name: Option<String>,
    tool_call_id: Option<String>,
    text: Option<String>,
    details: Value,
) -> Vec<Event> {
    if tool_name.as_deref() != Some("exec_command") {
        return Vec::new();
    }
    let details_obj = details.as_object();
    let command = details_obj
        .and_then(|details| details.get("cmd"))
        .and_then(string_or_none)
        .or_else(|| {
            details_obj
                .and_then(|details| details.get("command"))
                .and_then(string_or_none)
        });
    let exit_code = details_obj
        .and_then(|details| details.get("exit_code"))
        .and_then(|value| value.as_i64())
        .unwrap_or(0);
    let stderr = details_obj
        .and_then(|details| details.get("stderr"))
        .and_then(string_or_none);
    if text.is_none() && stderr.is_none() && details_obj.and_then(|d| d.get("exit_code")).is_none()
    {
        return Vec::new();
    }

    vec![session_event(
        &format!("evt_command_completed_{record_id}"),
        EventType::CommandCompleted,
        EventActor::System,
        timestamp,
        parent_id,
        json_object([
            (
                "command",
                command.unwrap_or_else(|| "exec_command".to_string()).into(),
            ),
            ("exit_code", exit_code.into()),
            ("stdout", text.map(Value::String).unwrap_or(Value::Null)),
            ("stderr", stderr.map(Value::String).unwrap_or(Value::Null)),
            (
                "tool_call_id",
                tool_call_id.map(Value::String).unwrap_or(Value::Null),
            ),
            ("source", "openclaw.session".into()),
        ]),
    )]
}

fn normalize_openclaw_custom_record(
    raw_item: &serde_json::Map<String, Value>,
    record_id: &str,
    parent_id: Option<String>,
    timestamp: Option<DateTime<Utc>>,
) -> Option<Event> {
    let tool_name = raw_item
        .get("name")
        .and_then(string_or_none)
        .or_else(|| raw_item.get("customType").and_then(string_or_none))
        .or_else(|| raw_item.get("event").and_then(string_or_none));
    let details = raw_item
        .get("data")
        .cloned()
        .filter(|value| value.is_object())
        .or_else(|| {
            raw_item
                .get("details")
                .cloned()
                .filter(|value| value.is_object())
        })
        .unwrap_or_else(|| Value::Object(Map::new()));
    let content = raw_item
        .get("text")
        .and_then(string_or_none)
        .or_else(|| raw_item.get("summary").and_then(string_or_none))
        .or_else(|| raw_item.get("content").and_then(string_or_none));

    if tool_name.is_none() && content.is_none() && details.as_object().is_none_or(|d| d.is_empty())
    {
        return None;
    }

    Some(session_event(
        &format!("evt_custom_{record_id}"),
        EventType::ToolCompleted,
        EventActor::Tool,
        timestamp,
        parent_id,
        json_object([
            (
                "tool_name",
                tool_name.unwrap_or_else(|| "custom".to_string()).into(),
            ),
            (
                "tool_call_id",
                raw_item
                    .get("toolCallId")
                    .and_then(string_or_none)
                    .map(Value::String)
                    .unwrap_or(Value::Null),
            ),
            ("content", content.map(Value::String).unwrap_or(Value::Null)),
            ("details", details),
            ("source", "openclaw.session.custom".into()),
        ]),
    ))
}

fn openclaw_session_id_from_import(events: &[Event], transcript_path: &std::path::Path) -> String {
    for event in events {
        if event.event_type != EventType::CaseStarted {
            continue;
        }
        if let Some(session_id) = event
            .payload
            .as_object()
            .and_then(|payload| payload.get("session_id"))
            .and_then(string_or_none)
        {
            return session_id;
        }
    }
    transcript_path
        .file_stem()
        .and_then(|item| item.to_str())
        .unwrap_or("openclaw-session")
        .to_string()
}

fn extract_openclaw_text_segments(content: &[Value]) -> Vec<String> {
    let mut segments = Vec::new();
    for item in content {
        let Some(item) = item.as_object() else {
            continue;
        };
        match item.get("type").and_then(string_or_none).as_deref() {
            Some("text") => {
                if let Some(text) = item.get("text").and_then(string_or_none) {
                    segments.push(text);
                }
            }
            Some("thinking") => {
                if let Some(thinking) = item.get("thinking").and_then(string_or_none) {
                    segments.push(thinking);
                }
            }
            _ => {}
        }
    }
    segments
}

fn extract_openclaw_visible_assistant_text(content: &[Value]) -> Vec<String> {
    let mut segments = Vec::new();
    for item in content {
        let Some(item) = item.as_object() else {
            continue;
        };
        match item.get("type").and_then(string_or_none).as_deref() {
            Some("text") => {
                if let Some(text) = item.get("text").and_then(string_or_none) {
                    segments.push(text);
                }
            }
            Some("thinking") => {
                if let Some(summary) = item.get("summary").and_then(|value| value.as_array()) {
                    for part in summary {
                        let Some(part) = part.as_object() else {
                            continue;
                        };
                        if part.get("type").and_then(string_or_none).as_deref()
                            != Some("summary_text")
                        {
                            continue;
                        }
                        if let Some(text) = part.get("text").and_then(string_or_none) {
                            segments.push(text);
                        }
                    }
                }
            }
            _ => {}
        }
    }
    segments
}

fn sanitize_openclaw_message_text(text: &str) -> Option<String> {
    let cleaned = text.replace("\r\n", "\n").trim().to_string();
    if cleaned.is_empty() {
        return None;
    }
    let mut kept_lines = Vec::new();
    let mut dropping_noise_block = false;
    for raw_line in cleaned.lines() {
        let line = raw_line.trim();
        let normalized = line.to_ascii_lowercase();
        if [
            "operator policy",
            "transport metadata",
            "[operator policy]",
            "[transport metadata]",
        ]
        .iter()
        .any(|prefix| normalized.starts_with(prefix))
        {
            dropping_noise_block = true;
            continue;
        }
        if dropping_noise_block {
            if line.is_empty() {
                dropping_noise_block = false;
            }
            continue;
        }
        kept_lines.push(raw_line.to_string());
    }
    let sanitized = kept_lines.join("\n").trim().to_string();
    (!sanitized.is_empty()).then_some(sanitized)
}

fn extract_file_reads_from_command(command: &str) -> Vec<String> {
    let tokens = match shlex::split(command) {
        Some(tokens) => tokens,
        None => return Vec::new(),
    };
    if tokens.is_empty() {
        return Vec::new();
    }
    match tokens[0].as_str() {
        "cat" | "head" | "tail" | "sed" => {
            dedupe_preserve_order(extract_path_like_tokens(&tokens[1..]))
        }
        "rg" | "grep" => dedupe_preserve_order(extract_search_command_paths(&tokens[1..])),
        _ => Vec::new(),
    }
}

fn extract_paths_from_apply_patch(patch_text: &str) -> Vec<String> {
    let mut paths = Vec::new();
    for raw_line in patch_text.lines() {
        let line = raw_line.trim();
        for prefix in [
            "*** Update File: ",
            "*** Add File: ",
            "*** Delete File: ",
            "*** Move to: ",
        ] {
            if let Some(path) = line.strip_prefix(prefix).map(str::trim) {
                if !path.is_empty() {
                    paths.push(path.to_string());
                }
            }
        }
    }
    dedupe_preserve_order(paths)
}

fn dedupe_preserve_order(values: Vec<String>) -> Vec<String> {
    let mut seen = HashSet::new();
    let mut deduped = Vec::new();
    for value in values {
        if seen.insert(value.clone()) {
            deduped.push(value);
        }
    }
    deduped
}

fn extract_path_like_tokens(tokens: &[String]) -> Vec<String> {
    tokens
        .iter()
        .filter(|token| !token.starts_with('-'))
        .filter(|token| {
            token.contains('/')
                || std::path::Path::new(token)
                    .file_name()
                    .and_then(|n| n.to_str())
                    .is_some_and(|name| name.contains('.'))
        })
        .cloned()
        .collect()
}

fn extract_search_command_paths(tokens: &[String]) -> Vec<String> {
    let mut paths = Vec::new();
    let mut saw_pattern = false;
    let mut skip_next = false;
    for token in tokens {
        if skip_next {
            skip_next = false;
            continue;
        }
        if ["-g", "-e", "-f", "--glob", "--regexp", "--file"].contains(&token.as_str()) {
            skip_next = true;
            continue;
        }
        if token.starts_with('-') {
            continue;
        }
        if !saw_pattern {
            saw_pattern = true;
            continue;
        }
        if token.contains('/')
            || std::path::Path::new(token)
                .file_name()
                .and_then(|n| n.to_str())
                .is_some_and(|name| name.contains('.'))
        {
            paths.push(token.clone());
        }
    }
    paths
}

fn parse_optional_timestamp(value: Option<&Value>) -> Result<Option<DateTime<Utc>>, String> {
    let Some(value) = value else {
        return Ok(None);
    };
    let Some(value) = value.as_str() else {
        return Err("timestamp must be an ISO-8601 string".to_string());
    };
    DateTime::parse_from_rfc3339(value)
        .map(|value| Some(value.with_timezone(&Utc)))
        .map_err(|error| error.to_string())
}

fn json_object<const N: usize>(pairs: [(&str, Value); N]) -> Value {
    let mut map = Map::new();
    for (key, value) in pairs {
        map.insert(key.to_string(), value);
    }
    Value::Object(map)
}

fn extract_decisions(case_id: &str, events: &[Event]) -> Vec<Decision> {
    let mut extracted = Vec::new();
    let mut seen_task_frame = false;
    let mut prior_user_messages: Vec<String> = Vec::new();

    for event in events {
        let payload = event.payload.as_object();
        match event.event_type {
            EventType::MessageUser => {
                let message = payload
                    .and_then(|payload| payload.get("message"))
                    .and_then(string_or_none);
                let is_new_user_intent = message.as_ref().is_some_and(|message| {
                    prior_user_messages.is_empty()
                        || normalize_message_intent(message)
                            != normalize_message_intent(
                                prior_user_messages.last().expect("prior user message"),
                            )
                });

                if let Some(message) = &message {
                    if let Some(prior_message) = prior_user_messages.last() {
                        if is_meaningful_clarification(message, prior_message) {
                            extracted.push(build_decision(
                                case_id,
                                DecisionType::ClarificationResolved,
                                "Task ambiguity resolved",
                                "How did follow-up guidance change the task understanding?",
                                message,
                                &[event.event_id.clone()],
                                &["Later user guidance can refine or narrow task understanding"],
                                "A meaningful follow-up user message changed the task framing compared with the earlier request.",
                                Some(message.clone()),
                                0.85,
                            ));
                        }
                    }
                    if is_new_user_intent && looks_like_constraint(message) {
                        extracted.push(build_decision(
                            case_id,
                            DecisionType::ConstraintAdopted,
                            "Constraint adopted",
                            "What constraint or guardrail is now part of the task?",
                            message,
                            &[event.event_id.clone()],
                            &["User-stated constraints should shape subsequent execution"],
                            "The user message introduced or narrowed a concrete task constraint.",
                            Some(message.clone()),
                            0.84,
                        ));
                    }
                    if is_new_user_intent && looks_like_success_criteria(message) {
                        extracted.push(build_decision(
                            case_id,
                            DecisionType::SuccessCriteriaSet,
                            "Success criteria established",
                            "What explicit standard now defines done or acceptable output?",
                            message,
                            &[event.event_id.clone()],
                            &["The task should be evaluated against explicit success criteria"],
                            "The user message made the expected output shape or acceptance bar explicit.",
                            Some(message.clone()),
                            0.83,
                        ));
                    }
                    if is_new_user_intent && looks_like_option_rejection(message) {
                        extracted.push(build_decision(
                            case_id,
                            DecisionType::OptionRejected,
                            "Option rejected",
                            "Which candidate path was explicitly ruled out?",
                            message,
                            &[event.event_id.clone()],
                            &["Rejected options should remain out of scope"],
                            "The message explicitly rejected one path in favor of a different direction.",
                            Some(message.clone()),
                            0.82,
                        ));
                    }
                    if is_new_user_intent && looks_like_authority_confirmation(message) {
                        let mut decision = build_decision(
                            case_id,
                            DecisionType::AuthorityConfirmed,
                            "Authority confirmed",
                            "What approval or decision authority was confirmed?",
                            message,
                            &[event.event_id.clone()],
                            &["Human approval established the allowed path forward"],
                            "The user message explicitly approved or authorized the current direction.",
                            Some(message.clone()),
                            0.86,
                        );
                        decision.requires_human_confirmation = true;
                        extracted.push(decision);
                    }
                    prior_user_messages.push(message.clone());
                }
            }
            EventType::UserConfirmed => {
                let chosen_action = payload
                    .and_then(|payload| payload.get("message"))
                    .and_then(string_or_none)
                    .unwrap_or_else(|| "Continue within the approved boundary".to_string());
                let outcome = payload
                    .and_then(|payload| payload.get("message"))
                    .and_then(string_or_none);
                let mut decision = build_decision(
                    case_id,
                    DecisionType::AuthorityConfirmed,
                    "Authority confirmed",
                    "What approval or decision authority was confirmed?",
                    &chosen_action,
                    &[event.event_id.clone()],
                    &["Human confirmation established the allowed path forward"],
                    "A user confirmation event signals explicit approval or authority for the chosen direction.",
                    outcome,
                    0.9,
                );
                decision.requires_human_confirmation = true;
                extracted.push(decision);
            }
            EventType::MessageAgent => {
                let Some(message) = payload
                    .and_then(|payload| payload.get("message"))
                    .and_then(string_or_none)
                else {
                    continue;
                };

                if !seen_task_frame && looks_like_task_frame(&message) {
                    extracted.push(build_decision(
                        case_id,
                        DecisionType::TaskFrameDefined,
                        "Task frame established",
                        "How is the task being framed for execution?",
                        &message,
                        &[event.event_id.clone()],
                        &["The first substantive agent framing sets the working interpretation of the task"],
                        "The agent explicitly restated how it understood the task and what boundary it would operate within.",
                        Some("Initial task frame captured from agent response".to_string()),
                        0.7,
                    ));
                    seen_task_frame = true;
                }
                if looks_like_option_rejection(&message) {
                    extracted.push(build_decision(
                        case_id,
                        DecisionType::OptionRejected,
                        "Alternative path rejected",
                        "Which path did the agent explicitly decide not to pursue?",
                        &message,
                        &[event.event_id.clone()],
                        &["Explicitly rejected paths should remain out of scope"],
                        "The agent message ruled out one approach while committing to another.",
                        Some(message.clone()),
                        0.77,
                    ));
                }
            }
            _ => {}
        }
    }

    extracted
        .into_iter()
        .enumerate()
        .map(|(index, mut decision)| {
            decision.sequence_no = (index + 1) as i64;
            decision
        })
        .collect()
}

fn build_decision(
    case_id: &str,
    decision_type: DecisionType,
    title: &str,
    question: &str,
    chosen_action: &str,
    evidence_event_ids: &[String],
    constraints: &[&str],
    selection_reason: &str,
    outcome: Option<String>,
    confidence: f64,
) -> Decision {
    let evidence_event_ids = evidence_event_ids.to_vec();
    let constraints = constraints
        .iter()
        .map(|value| value.to_string())
        .collect::<Vec<_>>();
    let explanation = DecisionExplanation {
        goal: question.to_string(),
        evidence: evidence_event_ids
            .iter()
            .map(|event_id| format!("event:{event_id}"))
            .collect(),
        constraints: constraints.clone(),
        selection_reason: selection_reason.to_string(),
        result: outcome.clone(),
    };

    Decision {
        decision_id: format!("dec_{}", &Uuid::new_v4().simple().to_string()[..12]),
        case_id: case_id.to_string(),
        decision_type,
        title: title.to_string(),
        question: question.to_string(),
        chosen_action: chosen_action.to_string(),
        alternatives: Vec::new(),
        evidence_event_ids,
        constraint_summary: if constraints.is_empty() {
            None
        } else {
            Some(constraints.join("; "))
        },
        requires_human_confirmation: false,
        outcome,
        confidence,
        explanation,
        sequence_no: 0,
    }
}

fn string_or_none(value: &Value) -> Option<String> {
    match value {
        Value::String(value) if !value.trim().is_empty() => Some(value.clone()),
        _ => None,
    }
}

fn is_meaningful_clarification(message: &str, prior_message: &str) -> bool {
    let current = normalize_message_intent(message);
    let previous = normalize_message_intent(prior_message);
    if current.is_empty() || previous.is_empty() {
        return current != previous;
    }
    if current == previous {
        return false;
    }

    let current_tokens = tokenize_keywords(&current);
    let previous_tokens = tokenize_keywords(&previous);
    if current_tokens.is_empty() || previous_tokens.is_empty() {
        return current != previous;
    }

    let shared = current_tokens.intersection(&previous_tokens).count();
    let overlap_ratio = shared as f64 / current_tokens.len().min(previous_tokens.len()) as f64;
    overlap_ratio < 0.8
}

fn normalize_message_intent(text: &str) -> String {
    text.split_whitespace()
        .map(|part| part.to_ascii_lowercase())
        .collect::<Vec<_>>()
        .join(" ")
}

fn tokenize_keywords(text: &str) -> HashSet<String> {
    let mut tokens = HashSet::new();
    let lower = text.to_ascii_lowercase();
    let mut current = String::new();
    for ch in lower.chars() {
        if ch.is_ascii_alphanumeric() || matches!(ch, '_' | '.' | '/' | '-') {
            current.push(ch);
        } else if !current.is_empty() {
            add_token(&mut tokens, &current);
            current.clear();
        }
    }
    if !current.is_empty() {
        add_token(&mut tokens, &current);
    }

    let expanded_tokens = tokens.clone();
    for token in expanded_tokens {
        for alias in semantic_aliases(&token) {
            tokens.insert(alias.to_string());
        }
    }
    tokens
}

fn add_token(tokens: &mut HashSet<String>, token: &str) {
    if token.len() >= 3 && !STOP_WORDS.contains(&token) {
        tokens.insert(token.to_string());
    }
    if token.contains(['/', '.', '-', '_']) {
        for part in token.split(['/', '.', '-', '_']) {
            if part.len() >= 3 && !STOP_WORDS.contains(&part) {
                tokens.insert(part.to_string());
            }
        }
    }
}

fn semantic_aliases(token: &str) -> &'static [&'static str] {
    match token {
        "bring" | "bringup" => &["readiness", "runtime"],
        "categories" | "category" | "class" | "stage" | "stages" | "state" | "states" => {
            &["classes"]
        }
        "differentiate" => &["split"],
        "followup" => &["required", "follow-up"],
        "handoff" | "needed" | "setup" | "wiring" => &["required"],
        "images" => &["imported"],
        "operators" => &["operator"],
        "restored" => &["restore", "imported"],
        _ => &[],
    }
}

fn derive_artifacts(
    store: &SqliteStore,
    case_id: &str,
    events: &[Event],
) -> Result<Vec<Artifact>, openprecedent_store_sqlite::SqliteStoreError> {
    let mut derived = Vec::new();
    let mut seen_ids = HashSet::new();

    for event in events {
        let payload = event.payload.as_object();
        let artifact = match event.event_type {
            EventType::FileWrite => payload
                .and_then(|payload| payload.get("path"))
                .and_then(string_or_none)
                .map(|path| Artifact {
                    artifact_id: format!("artifact_{}", event.event_id),
                    case_id: case_id.to_string(),
                    artifact_type: ArtifactType::File,
                    uri_or_path: path,
                    summary: payload
                        .and_then(|payload| payload.get("summary"))
                        .and_then(string_or_none),
                }),
            EventType::CommandCompleted => payload
                .and_then(|payload| payload.get("command"))
                .and_then(string_or_none)
                .map(|command| Artifact {
                    artifact_id: format!("artifact_{}", event.event_id),
                    case_id: case_id.to_string(),
                    artifact_type: ArtifactType::CommandOutput,
                    uri_or_path: command,
                    summary: payload
                        .and_then(|payload| payload.get("stdout"))
                        .and_then(string_or_none)
                        .or_else(|| {
                            payload
                                .and_then(|payload| payload.get("stderr"))
                                .and_then(string_or_none)
                        }),
                }),
            EventType::MessageUser | EventType::MessageAgent => payload
                .and_then(|payload| payload.get("message"))
                .and_then(string_or_none)
                .map(|message| Artifact {
                    artifact_id: format!("artifact_{}", event.event_id),
                    case_id: case_id.to_string(),
                    artifact_type: ArtifactType::Message,
                    uri_or_path: format!("{}:{}", event.event_type, event.event_id),
                    summary: Some(message),
                }),
            _ => None,
        };

        let Some(artifact) = artifact else {
            continue;
        };
        if seen_ids.contains(&artifact.artifact_id) {
            continue;
        }
        store.upsert_artifact(&artifact)?;
        seen_ids.insert(artifact.artifact_id.clone());
        derived.push(artifact);
    }

    Ok(derived)
}

fn build_case_summary(case: &Case, events: &[Event], decisions: &[Decision]) -> String {
    format!(
        "{}: {} events, {} decisions, status={}",
        case.title,
        events.len(),
        decisions.len(),
        case.status
    )
}

#[derive(Debug)]
struct CaseFingerprint {
    status: String,
    has_file_write: bool,
    has_recovery: bool,
    tool_count: i64,
    tool_names: HashSet<String>,
    file_paths: HashSet<String>,
    file_read_paths: HashSet<String>,
    keywords: HashSet<String>,
    decision_keywords: HashSet<String>,
    decision_types: HashSet<String>,
}

fn build_case_fingerprint(
    case: &Case,
    events: &[Event],
    decisions: &[Decision],
) -> CaseFingerprint {
    let mut tool_names = HashSet::new();
    let mut file_paths = HashSet::new();
    let mut file_read_paths = HashSet::new();
    let mut tool_count = 0_i64;
    let mut has_file_write = false;
    let mut has_recovery = false;

    for event in events {
        let payload = event.payload.as_object();
        if event.event_type == EventType::ToolCalled {
            tool_count += 1;
        }
        if event.event_type == EventType::FileWrite {
            has_file_write = true;
        }
        if event.event_type == EventType::CommandCompleted {
            if let Some(exit_code) = payload
                .and_then(|payload| payload.get("exit_code"))
                .and_then(|value| value.as_i64())
            {
                if exit_code != 0 {
                    has_recovery = true;
                }
            }
        }

        if let Some(tool_name) = payload
            .and_then(|payload| payload.get("tool_name"))
            .and_then(string_or_none)
        {
            tool_names.insert(tool_name);
        }
        if let Some(path) = payload
            .and_then(|payload| payload.get("path"))
            .and_then(string_or_none)
        {
            let name = std::path::Path::new(&path)
                .file_name()
                .and_then(|item| item.to_str())
                .unwrap_or(&path)
                .to_string();
            file_paths.insert(name.clone());
            if event.event_type == EventType::FileRead {
                file_read_paths.insert(name);
            }
        }
    }

    CaseFingerprint {
        status: case.status.to_string(),
        has_file_write,
        has_recovery,
        tool_count,
        tool_names,
        file_paths,
        file_read_paths,
        keywords: case_keywords(case, events, decisions),
        decision_keywords: decision_keywords(decisions),
        decision_types: decisions
            .iter()
            .map(|decision| decision.decision_type.to_string())
            .collect(),
    }
}

fn compare_fingerprints(
    current: &CaseFingerprint,
    other: &CaseFingerprint,
) -> (i64, Vec<String>, Vec<String>) {
    let mut score = 0_i64;
    let mut similarities = Vec::new();
    let mut differences = Vec::new();

    if current.status == other.status {
        score += 1;
        similarities.push("same status".to_string());
    } else {
        differences.push("different status".to_string());
    }

    for (key, left, right) in [
        (
            "has_file_write",
            current.has_file_write,
            other.has_file_write,
        ),
        ("has_recovery", current.has_recovery, other.has_recovery),
    ] {
        if left == right {
            if left {
                score += 1;
                similarities.push(format!("same {key}"));
            }
        } else {
            differences.push(format!("different {key}"));
        }
    }

    if current.decision_types == other.decision_types {
        score += 6;
        similarities.push("same decision shape".to_string());
    } else {
        let shared_decisions = intersection_sorted(&current.decision_types, &other.decision_types);
        if !shared_decisions.is_empty() {
            score += (shared_decisions.len() as i64 * 2).min(6);
            similarities.push(format!(
                "shared decision types: {}",
                shared_decisions.join(",")
            ));
        } else {
            differences.push("different decision shape".to_string());
        }
    }

    let shared_decision_keywords =
        intersection_sorted(&current.decision_keywords, &other.decision_keywords);
    if !shared_decision_keywords.is_empty() {
        score += (shared_decision_keywords.len() as i64 * 2).min(8);
        similarities.push(format!(
            "shared decision language: {}",
            shared_decision_keywords
                .iter()
                .take(4)
                .cloned()
                .collect::<Vec<_>>()
                .join(",")
        ));
    } else {
        differences.push("different decision language".to_string());
    }

    let tool_delta = (current.tool_count - other.tool_count).abs();
    if tool_delta == 0 {
        score += 1;
        similarities.push("same tool call count".to_string());
    } else if tool_delta == 1 {
        similarities.push("nearby tool call count".to_string());
    } else {
        differences.push("different tool call count".to_string());
    }

    let shared_tools = intersection_sorted(&current.tool_names, &other.tool_names);
    if !shared_tools.is_empty() {
        score += 1;
        similarities.push(format!(
            "shared tools: {}",
            shared_tools
                .iter()
                .take(3)
                .cloned()
                .collect::<Vec<_>>()
                .join(",")
        ));
    } else {
        differences.push("different tools".to_string());
    }

    let shared_paths = intersection_sorted(&current.file_paths, &other.file_paths);
    if !shared_paths.is_empty() {
        score += 1;
        similarities.push(format!(
            "shared file targets: {}",
            shared_paths
                .iter()
                .take(3)
                .cloned()
                .collect::<Vec<_>>()
                .join(",")
        ));
    }

    let shared_read_paths = intersection_sorted(&current.file_read_paths, &other.file_read_paths);
    if !shared_read_paths.is_empty() {
        score += (shared_read_paths.len() as i64).min(2);
        similarities.push(format!(
            "shared read targets: {}",
            shared_read_paths
                .iter()
                .take(3)
                .cloned()
                .collect::<Vec<_>>()
                .join(",")
        ));
    }

    let shared_keywords = intersection_sorted(&current.keywords, &other.keywords);
    if !shared_keywords.is_empty() {
        score += (shared_keywords.len() as i64).min(4);
        similarities.push(format!(
            "shared keywords: {}",
            shared_keywords
                .iter()
                .take(4)
                .cloned()
                .collect::<Vec<_>>()
                .join(",")
        ));
    } else {
        differences.push("different task keywords".to_string());
    }

    let clarification = DecisionType::ClarificationResolved.to_string();
    let clarification_mismatch = current.decision_types.contains(&clarification)
        ^ other.decision_types.contains(&clarification);
    if clarification_mismatch {
        score -= 1;
        differences.push("different clarification pattern".to_string());
    }

    if similarities.is_empty() {
        similarities.push("similar case structure".to_string());
    }

    (score, similarities, differences)
}

fn case_keywords(case: &Case, events: &[Event], decisions: &[Decision]) -> HashSet<String> {
    let mut texts = vec![case.title.clone()];
    if let Some(summary) = &case.final_summary {
        texts.push(summary.clone());
    }

    for event in events {
        if let Some(payload) = event.payload.as_object() {
            for key in ["message", "path", "tool_name", "command"] {
                if let Some(value) = payload.get(key).and_then(string_or_none) {
                    texts.push(value);
                }
            }
        }
    }
    for decision in decisions {
        texts.push(decision.title.clone());
        texts.push(decision.chosen_action.clone());
        if let Some(outcome) = &decision.outcome {
            texts.push(outcome.clone());
        }
    }

    let mut keywords = HashSet::new();
    for text in texts {
        keywords.extend(tokenize_keywords(&text));
    }
    keywords
}

fn decision_keywords(decisions: &[Decision]) -> HashSet<String> {
    let mut keywords = HashSet::new();
    for decision in decisions {
        keywords.extend(tokenize_keywords(&decision.title));
        keywords.extend(tokenize_keywords(&decision.chosen_action));
        if let Some(outcome) = &decision.outcome {
            keywords.extend(tokenize_keywords(outcome));
        }
    }
    keywords
}

fn build_reusable_takeaway(case: &Case, decisions: &[Decision]) -> Option<String> {
    decisions
        .last()
        .map(|decision| decision.chosen_action.clone())
        .or_else(|| case.final_summary.clone())
}

fn intersection_sorted(left: &HashSet<String>, right: &HashSet<String>) -> Vec<String> {
    let mut values = left.intersection(right).cloned().collect::<Vec<_>>();
    values.sort();
    values
}

fn looks_like_task_frame(message: &str) -> bool {
    let normalized = normalize_message_intent(message);
    normalized.starts_with("i will ")
        || normalized.starts_with("i'll ")
        || normalized.starts_with("i can ")
        || normalized.starts_with("i found ")
        || normalized.starts_with("i am going to ")
        || normalized.starts_with("i'm going to ")
        || normalized.starts_with("let me ")
        || normalized.contains(" i will ")
}

fn looks_like_constraint(message: &str) -> bool {
    let normalized = normalize_message_intent(message);
    [
        "focus on",
        "only ",
        "do not",
        "don't",
        "without ",
        "must ",
        "need to",
        "avoid ",
        "instead of",
    ]
    .iter()
    .any(|marker| normalized.contains(marker))
}

fn looks_like_success_criteria(message: &str) -> bool {
    let normalized = normalize_message_intent(message);
    [
        "done when",
        "success means",
        "return ",
        "provide ",
        "give me",
        "output ",
        "summary ",
        "summarize ",
        "nothing else",
    ]
    .iter()
    .any(|marker| normalized.contains(marker))
}

fn looks_like_option_rejection(message: &str) -> bool {
    let normalized = normalize_message_intent(message);
    ["do not", "don't", "instead of", "rather than", "skip "]
        .iter()
        .any(|marker| normalized.contains(marker))
}

fn looks_like_authority_confirmation(message: &str) -> bool {
    let normalized = normalize_message_intent(message);
    [
        "approved",
        "approval granted",
        "go ahead",
        "you can proceed",
        "proceed with",
        "continue with",
        "continue within",
    ]
    .iter()
    .any(|marker| normalized.contains(marker))
}

const STOP_WORDS: [&str; 18] = [
    "the", "and", "for", "with", "that", "this", "from", "into", "will", "then", "case",
    "openclaw", "session", "docs", "file", "tool", "command", "agent",
];

fn capture_path(command: CaptureCommand) -> Vec<&'static str> {
    match command.runtime {
        CaptureRuntime::Openclaw(command) => match command.command {
            OpenclawCaptureSubcommand::ListSessions(_) => {
                vec!["capture", "openclaw", "list-sessions"]
            }
            OpenclawCaptureSubcommand::ImportSession(_) => {
                vec!["capture", "openclaw", "import-session"]
            }
            OpenclawCaptureSubcommand::CollectSessions(_) => {
                vec!["capture", "openclaw", "collect-sessions"]
            }
            OpenclawCaptureSubcommand::ImportJsonl(_) => {
                vec!["capture", "openclaw", "import-jsonl"]
            }
        },
        CaptureRuntime::Codex(command) => match command.command {
            CodexCaptureSubcommand::ImportRollout(_) => vec!["capture", "codex", "import-rollout"],
        },
    }
}

fn lineage_path(command: LineageCommand) -> Vec<&'static str> {
    match command.command {
        LineageSubcommand::Brief(_) => vec!["lineage", "brief"],
        LineageSubcommand::Invocation(command) => match command.command {
            LineageInvocationSubcommand::List(_) => vec!["lineage", "invocation", "list"],
            LineageInvocationSubcommand::Inspect(_) => vec!["lineage", "invocation", "inspect"],
        },
    }
}

fn eval_path(command: EvalCommand) -> Vec<&'static str> {
    match command.command {
        EvalSubcommand::Fixtures(_) => vec!["eval", "fixtures"],
        EvalSubcommand::CapturedOpenclawSessions(_) => vec!["eval", "captured-openclaw-sessions"],
    }
}
