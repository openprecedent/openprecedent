use openprecedent_contracts::CLI_BINARY_NAME;

#[derive(Debug, thiserror::Error)]
pub enum BootstrapError {
    #[error("command execution is not implemented yet for {0}")]
    NotImplemented(String),
}

pub fn not_implemented(command_path: &[&str]) -> BootstrapError {
    let joined = command_path.join(" ");
    BootstrapError::NotImplemented(format!("{CLI_BINARY_NAME} {joined}"))
}
