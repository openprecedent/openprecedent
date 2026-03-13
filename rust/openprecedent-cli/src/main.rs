use clap::{Args, Parser, Subcommand};
use openprecedent_contracts::{CLI_BINARY_NAME, CONTRACT_PHASE};
use openprecedent_core::not_implemented;

#[derive(Debug, Parser)]
#[command(name = CLI_BINARY_NAME)]
#[command(about = "Stable public CLI for OpenPrecedent")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    Case(DomainAction),
    Event(DomainAction),
    Decision(DomainAction),
    Replay(DomainAction),
    Precedent(DomainAction),
    Capture(CaptureCommand),
    Lineage(LineageCommand),
    Eval(DomainAction),
    Doctor(DoctorCommand),
    Version,
}

#[derive(Debug, Args)]
struct DomainAction {
    #[arg(trailing_var_arg = true)]
    args: Vec<String>,
}

#[derive(Debug, Subcommand)]
enum CaptureRuntime {
    Openclaw(RuntimeAction),
    Codex(RuntimeAction),
}

#[derive(Debug, Args)]
struct CaptureCommand {
    #[command(subcommand)]
    runtime: CaptureRuntime,
}

#[derive(Debug, Args)]
struct RuntimeAction {
    #[arg(trailing_var_arg = true)]
    args: Vec<String>,
}

#[derive(Debug, Subcommand)]
enum LineageSubcommand {
    Brief(RuntimeAction),
    Invocation(LineageInvocationCommand),
}

#[derive(Debug, Args)]
struct LineageCommand {
    #[command(subcommand)]
    command: LineageSubcommand,
}

#[derive(Debug, Subcommand)]
enum LineageInvocationSubcommand {
    List(RuntimeAction),
    Inspect(RuntimeAction),
}

#[derive(Debug, Args)]
struct LineageInvocationCommand {
    #[command(subcommand)]
    command: LineageInvocationSubcommand,
}

#[derive(Debug, Subcommand)]
enum DoctorSubcommand {
    Paths(RuntimeAction),
    Storage(RuntimeAction),
    Environment(RuntimeAction),
}

#[derive(Debug, Args)]
struct DoctorCommand {
    #[command(subcommand)]
    command: DoctorSubcommand,
}

fn main() {
    let cli = Cli::parse();
    let exit_code = match cli.command {
        Command::Case(_) => render_not_implemented(&["case"]),
        Command::Event(_) => render_not_implemented(&["event"]),
        Command::Decision(_) => render_not_implemented(&["decision"]),
        Command::Replay(_) => render_not_implemented(&["replay"]),
        Command::Precedent(_) => render_not_implemented(&["precedent"]),
        Command::Capture(command) => match command.runtime {
            CaptureRuntime::Openclaw(_) => render_not_implemented(&["capture", "openclaw"]),
            CaptureRuntime::Codex(_) => render_not_implemented(&["capture", "codex"]),
        },
        Command::Lineage(command) => match command.command {
            LineageSubcommand::Brief(_) => render_not_implemented(&["lineage", "brief"]),
            LineageSubcommand::Invocation(command) => match command.command {
                LineageInvocationSubcommand::List(_) => {
                    render_not_implemented(&["lineage", "invocation", "list"])
                }
                LineageInvocationSubcommand::Inspect(_) => {
                    render_not_implemented(&["lineage", "invocation", "inspect"])
                }
            },
        },
        Command::Eval(_) => render_not_implemented(&["eval"]),
        Command::Doctor(command) => match command.command {
            DoctorSubcommand::Paths(_) => render_not_implemented(&["doctor", "paths"]),
            DoctorSubcommand::Storage(_) => render_not_implemented(&["doctor", "storage"]),
            DoctorSubcommand::Environment(_) => render_not_implemented(&["doctor", "environment"]),
        },
        Command::Version => {
            println!(
                "{CLI_BINARY_NAME} {} ({CONTRACT_PHASE})",
                env!("CARGO_PKG_VERSION")
            );
            0
        }
    };

    std::process::exit(exit_code);
}

fn render_not_implemented(command_path: &[&str]) -> i32 {
    eprintln!("{}", not_implemented(command_path));
    1
}
