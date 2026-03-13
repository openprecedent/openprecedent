use std::collections::HashSet;
use std::ffi::OsString;
use std::fs::File;
use std::io::{BufRead, BufReader};

use chrono::{DateTime, Utc};
use clap::{ArgAction, Args, CommandFactory, FromArgMatches, Parser, Subcommand};
use openprecedent_contracts::{
    Case, CaseStatus, Decision, DecisionExplanation, DecisionType, Event, EventActor, EventType,
    OutputFormat, PathsDoctorReport, StorageDoctorReport, VersionReport, CLI_BINARY_NAME,
    CONTRACT_PHASE,
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
    Case(TrailingArgs),
}

#[derive(Debug, Args)]
struct PrecedentCommand {
    #[command(subcommand)]
    command: PrecedentSubcommand,
}

#[derive(Debug, Subcommand)]
enum PrecedentSubcommand {
    Find(TrailingArgs),
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
    ListSessions(TrailingArgs),
    ImportSession(TrailingArgs),
    CollectSessions(TrailingArgs),
    ImportJsonl(TrailingArgs),
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
        Command::Replay(command) => render_not_implemented_path(replay_path(command)),
        Command::Precedent(command) => render_not_implemented_path(precedent_path(command)),
        Command::Capture(command) => render_not_implemented_path(capture_path(command)),
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

fn replay_path(command: ReplayCommand) -> Vec<&'static str> {
    match command.command {
        ReplaySubcommand::Case(_) => vec!["replay", "case"],
    }
}

fn precedent_path(command: PrecedentCommand) -> Vec<&'static str> {
    match command.command {
        PrecedentSubcommand::Find(_) => vec!["precedent", "find"],
    }
}

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
