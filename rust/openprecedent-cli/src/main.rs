use std::ffi::OsString;

use clap::{ArgAction, Args, CommandFactory, FromArgMatches, Parser, Subcommand};
use openprecedent_contracts::{
    OutputFormat, PathsDoctorReport, StorageDoctorReport, VersionReport, CLI_BINARY_NAME,
    CONTRACT_PHASE,
};
use openprecedent_core::{
    build_environment_report, build_paths_report, build_storage_report, build_version_report,
    not_implemented, resolve_runtime_config, CliConfigOverrides,
};
use serde::Serialize;

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
    Create(TrailingArgs),
    List(TrailingArgs),
    Show(TrailingArgs),
}

#[derive(Debug, Args)]
struct EventCommand {
    #[command(subcommand)]
    command: EventSubcommand,
}

#[derive(Debug, Subcommand)]
enum EventSubcommand {
    Append(TrailingArgs),
    ImportJsonl(TrailingArgs),
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
        Command::Case(command) => render_not_implemented_path(case_path(command)),
        Command::Event(command) => render_not_implemented_path(event_path(command)),
        Command::Decision(command) => render_not_implemented_path(decision_path(command)),
        Command::Replay(command) => render_not_implemented_path(replay_path(command)),
        Command::Precedent(command) => render_not_implemented_path(precedent_path(command)),
        Command::Capture(command) => render_not_implemented_path(capture_path(command)),
        Command::Lineage(command) => render_not_implemented_path(lineage_path(command)),
        Command::Eval(command) => render_not_implemented_path(eval_path(command)),
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

trait TextRenderable {
    fn render_text(&self) -> String;
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

fn case_path(command: CaseCommand) -> Vec<&'static str> {
    match command.command {
        CaseSubcommand::Create(_) => vec!["case", "create"],
        CaseSubcommand::List(_) => vec!["case", "list"],
        CaseSubcommand::Show(_) => vec!["case", "show"],
    }
}

fn event_path(command: EventCommand) -> Vec<&'static str> {
    match command.command {
        EventSubcommand::Append(_) => vec!["event", "append"],
        EventSubcommand::ImportJsonl(_) => vec!["event", "import-jsonl"],
    }
}

fn decision_path(command: DecisionCommand) -> Vec<&'static str> {
    match command.command {
        DecisionSubcommand::Extract(_) => vec!["decision", "extract"],
        DecisionSubcommand::List(_) => vec!["decision", "list"],
    }
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
