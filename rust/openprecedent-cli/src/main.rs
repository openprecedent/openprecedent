use std::ffi::OsString;
use std::fs::File;
use std::io::{BufRead, BufReader};

use chrono::{DateTime, Utc};
use clap::{ArgAction, Args, CommandFactory, FromArgMatches, Parser, Subcommand};
use openprecedent_contracts::{
    Case, CaseStatus, Event, EventActor, EventType, OutputFormat, PathsDoctorReport,
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
    Extract(TrailingArgs),
    List(TrailingArgs),
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
        Command::Decision(command) => render_not_implemented_path(decision_path(command)),
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

fn decision_path(command: DecisionCommand) -> Vec<&'static str> {
    match command.command {
        DecisionSubcommand::Extract(_) => vec!["decision", "extract"],
        DecisionSubcommand::List(_) => vec!["decision", "list"],
    }
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
