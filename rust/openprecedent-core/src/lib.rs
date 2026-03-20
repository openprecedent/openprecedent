use std::env;
use std::fs;
use std::path::{Path, PathBuf};

use openprecedent_contracts::{
    ConfigFileReport, ConfigSource, EnvironmentDoctorReport, EnvironmentVariableReport,
    OutputFormat, PathsDoctorReport, ResolvedPath, ResolvedValue, StorageDoctorReport,
    StoragePathReport, VersionReport, CLI_BINARY_NAME, COLLECTOR_STATE_ENV_VAR, DB_ENV_VAR,
    DEFAULT_COLLECTOR_STATE_NAME, DEFAULT_DB_NAME, DEFAULT_RUNTIME_INVOCATION_LOG_NAME,
    FORMAT_ENV_VAR, HOME_ENV_VAR, NO_COLOR_ENV_VAR, RUNTIME_INVOCATION_LOG_ENV_VAR,
};
use serde::Deserialize;

#[derive(Debug, thiserror::Error)]
pub enum BootstrapError {
    #[error("command execution is not implemented yet for {0}")]
    NotImplemented(String),
    #[error("failed to resolve current working directory: {0}")]
    CurrentDirectory(String),
    #[error("home directory is unavailable for the Rust CLI default runtime home")]
    HomeDirectoryUnavailable,
    #[error("config file does not exist: {0}")]
    MissingConfigFile(String),
    #[error("failed to read config file {path}: {message}")]
    ReadConfigFile { path: String, message: String },
    #[error("failed to parse config file {path}: {message}")]
    ParseConfigFile { path: String, message: String },
    #[error("invalid value for OPENPRECEDENT_FORMAT: {0}")]
    InvalidFormat(String),
    #[error("invalid value for OPENPRECEDENT_NO_COLOR: {0}")]
    InvalidBool(String),
}

pub fn not_implemented(command_path: &[&str]) -> BootstrapError {
    let joined = command_path.join(" ");
    BootstrapError::NotImplemented(format!("{CLI_BINARY_NAME} {joined}"))
}

#[derive(Debug, Clone)]
pub struct CliConfigOverrides {
    pub format: Option<OutputFormat>,
    pub no_color: bool,
    pub home: Option<PathBuf>,
    pub db: Option<PathBuf>,
    pub invocation_log: Option<PathBuf>,
    pub state_file: Option<PathBuf>,
    pub config: Option<PathBuf>,
}

#[derive(Debug, Clone)]
pub struct ResolvedRuntimeConfig {
    pub format: ResolvedValue<OutputFormat>,
    pub no_color: ResolvedValue<bool>,
    pub config_file: Option<ConfigFileReport>,
    pub home: ResolvedPath,
    pub db: ResolvedPath,
    pub invocation_log: ResolvedPath,
    pub state_file: ResolvedPath,
}

#[derive(Debug, Default, Deserialize)]
struct FileConfig {
    format: Option<OutputFormat>,
    no_color: Option<bool>,
    home: Option<PathBuf>,
    db: Option<PathBuf>,
    invocation_log: Option<PathBuf>,
    state_file: Option<PathBuf>,
}

pub fn resolve_runtime_config(
    overrides: &CliConfigOverrides,
) -> Result<ResolvedRuntimeConfig, BootstrapError> {
    let config_input = load_config_file(overrides.config.as_deref())?;

    let format = if let Some(value) = overrides.format {
        ResolvedValue {
            value,
            source: ConfigSource::Flag,
        }
    } else if let Some(value) = env::var_os(FORMAT_ENV_VAR) {
        ResolvedValue {
            value: parse_output_format(&value.to_string_lossy())?,
            source: ConfigSource::Env,
        }
    } else if let Some(value) = config_input.file_config.format {
        ResolvedValue {
            value,
            source: ConfigSource::ConfigFile,
        }
    } else {
        ResolvedValue {
            value: OutputFormat::Text,
            source: ConfigSource::Default,
        }
    };

    let no_color = if overrides.no_color {
        ResolvedValue {
            value: true,
            source: ConfigSource::Flag,
        }
    } else if let Some(value) = env::var_os(NO_COLOR_ENV_VAR) {
        ResolvedValue {
            value: parse_bool(&value.to_string_lossy())?,
            source: ConfigSource::Env,
        }
    } else if let Some(value) = config_input.file_config.no_color {
        ResolvedValue {
            value,
            source: ConfigSource::ConfigFile,
        }
    } else {
        ResolvedValue {
            value: false,
            source: ConfigSource::Default,
        }
    };

    let home = if let Some(value) = overrides.home.as_deref() {
        ResolvedPath {
            path: normalize_path(value, None)?,
            source: ConfigSource::Flag,
            derived_from: None,
        }
    } else if let Some(value) = env::var_os(HOME_ENV_VAR) {
        ResolvedPath {
            path: normalize_path(Path::new(&value), None)?,
            source: ConfigSource::Env,
            derived_from: None,
        }
    } else if let Some(value) = config_input.file_config.home.as_deref() {
        ResolvedPath {
            path: normalize_path(value, config_input.base_dir.as_deref())?,
            source: ConfigSource::ConfigFile,
            derived_from: None,
        }
    } else {
        ResolvedPath {
            path: default_runtime_home()?,
            source: ConfigSource::Default,
            derived_from: None,
        }
    };

    let db = resolve_path(
        overrides.db.as_deref(),
        DB_ENV_VAR,
        config_input.file_config.db.as_deref(),
        config_input.base_dir.as_deref(),
        &home,
        DEFAULT_DB_NAME,
    )?;
    let invocation_log = resolve_path(
        overrides.invocation_log.as_deref(),
        RUNTIME_INVOCATION_LOG_ENV_VAR,
        config_input.file_config.invocation_log.as_deref(),
        config_input.base_dir.as_deref(),
        &home,
        DEFAULT_RUNTIME_INVOCATION_LOG_NAME,
    )?;
    let state_file = resolve_path(
        overrides.state_file.as_deref(),
        COLLECTOR_STATE_ENV_VAR,
        config_input.file_config.state_file.as_deref(),
        config_input.base_dir.as_deref(),
        &home,
        DEFAULT_COLLECTOR_STATE_NAME,
    )?;

    Ok(ResolvedRuntimeConfig {
        format,
        no_color,
        config_file: config_input.report,
        home,
        db,
        invocation_log,
        state_file,
    })
}

pub fn build_paths_report(config: &ResolvedRuntimeConfig) -> PathsDoctorReport {
    PathsDoctorReport {
        config_file: config.config_file.clone(),
        home: config.home.clone(),
        db: config.db.clone(),
        invocation_log: config.invocation_log.clone(),
        state_file: config.state_file.clone(),
    }
}

pub fn build_storage_report(config: &ResolvedRuntimeConfig) -> StorageDoctorReport {
    StorageDoctorReport {
        db: storage_path_report(&config.db),
        invocation_log: storage_path_report(&config.invocation_log),
        state_file: storage_path_report(&config.state_file),
    }
}

pub fn build_environment_report(config: &ResolvedRuntimeConfig) -> EnvironmentDoctorReport {
    EnvironmentDoctorReport {
        format: config.format.clone(),
        no_color: config.no_color.clone(),
        config_file: config.config_file.clone(),
        variables: vec![
            env_var_report(HOME_ENV_VAR),
            env_var_report(DB_ENV_VAR),
            env_var_report(RUNTIME_INVOCATION_LOG_ENV_VAR),
            env_var_report(COLLECTOR_STATE_ENV_VAR),
            env_var_report(FORMAT_ENV_VAR),
            env_var_report(NO_COLOR_ENV_VAR),
        ],
    }
}

pub fn build_version_report(version: &'static str, contract_phase: &'static str) -> VersionReport {
    VersionReport {
        name: CLI_BINARY_NAME,
        version,
        contract_phase,
    }
}

fn storage_path_report(path: &ResolvedPath) -> StoragePathReport {
    let parent_exists = path.path.parent().is_some_and(Path::exists);
    StoragePathReport {
        path: path.path.clone(),
        source: path.source,
        derived_from: path.derived_from,
        exists: path.path.exists(),
        parent_exists,
    }
}

fn env_var_report(name: &'static str) -> EnvironmentVariableReport {
    let value = env::var(name).ok();
    EnvironmentVariableReport {
        name,
        is_set: value.is_some(),
        value,
    }
}

struct LoadedConfig {
    file_config: FileConfig,
    report: Option<ConfigFileReport>,
    base_dir: Option<PathBuf>,
}

fn load_config_file(path: Option<&Path>) -> Result<LoadedConfig, BootstrapError> {
    let Some(path) = path else {
        return Ok(LoadedConfig {
            file_config: FileConfig::default(),
            report: None,
            base_dir: None,
        });
    };

    let resolved_path = normalize_path(path, None)?;
    if !resolved_path.exists() {
        return Err(BootstrapError::MissingConfigFile(
            resolved_path.display().to_string(),
        ));
    }

    let contents =
        fs::read_to_string(&resolved_path).map_err(|error| BootstrapError::ReadConfigFile {
            path: resolved_path.display().to_string(),
            message: error.to_string(),
        })?;
    let file_config = toml::from_str::<FileConfig>(&contents).map_err(|error| {
        BootstrapError::ParseConfigFile {
            path: resolved_path.display().to_string(),
            message: error.to_string(),
        }
    })?;

    Ok(LoadedConfig {
        file_config,
        report: Some(ConfigFileReport {
            path: resolved_path.clone(),
            exists: true,
        }),
        base_dir: resolved_path.parent().map(Path::to_path_buf),
    })
}

fn resolve_path(
    flag_value: Option<&Path>,
    env_name: &str,
    config_value: Option<&Path>,
    config_base_dir: Option<&Path>,
    home: &ResolvedPath,
    fallback_name: &str,
) -> Result<ResolvedPath, BootstrapError> {
    if let Some(value) = flag_value {
        return Ok(ResolvedPath {
            path: normalize_path(value, None)?,
            source: ConfigSource::Flag,
            derived_from: None,
        });
    }
    if let Some(value) = env::var_os(env_name) {
        return Ok(ResolvedPath {
            path: normalize_path(Path::new(&value), None)?,
            source: ConfigSource::Env,
            derived_from: None,
        });
    }
    if let Some(value) = config_value {
        return Ok(ResolvedPath {
            path: normalize_path(value, config_base_dir)?,
            source: ConfigSource::ConfigFile,
            derived_from: None,
        });
    }
    Ok(ResolvedPath {
        path: home.path.join(fallback_name),
        source: home.source,
        derived_from: Some("home"),
    })
}

fn normalize_path(value: &Path, base_dir: Option<&Path>) -> Result<PathBuf, BootstrapError> {
    let as_string = value.to_string_lossy();
    let expanded = if let Some(stripped) = as_string.strip_prefix("~/") {
        home_dir()?.join(stripped)
    } else if as_string == "~" {
        home_dir()?
    } else if value.is_absolute() {
        value.to_path_buf()
    } else {
        let base = match base_dir {
            Some(path) => path.to_path_buf(),
            None => env::current_dir()
                .map_err(|error| BootstrapError::CurrentDirectory(error.to_string()))?,
        };
        base.join(value)
    };
    Ok(expanded)
}

fn home_dir() -> Result<PathBuf, BootstrapError> {
    let Some(home) = env::var_os("HOME") else {
        return Err(BootstrapError::HomeDirectoryUnavailable);
    };
    Ok(PathBuf::from(home))
}

fn default_runtime_home() -> Result<PathBuf, BootstrapError> {
    Ok(home_dir()?.join(".openprecedent").join("runtime"))
}

fn parse_output_format(value: &str) -> Result<OutputFormat, BootstrapError> {
    match value {
        "json" => Ok(OutputFormat::Json),
        "text" => Ok(OutputFormat::Text),
        other => Err(BootstrapError::InvalidFormat(other.to_string())),
    }
}

fn parse_bool(value: &str) -> Result<bool, BootstrapError> {
    match value.to_ascii_lowercase().as_str() {
        "1" | "true" | "yes" | "on" => Ok(true),
        "0" | "false" | "no" | "off" => Ok(false),
        other => Err(BootstrapError::InvalidBool(other.to_string())),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::{SystemTime, UNIX_EPOCH};

    fn unique_temp_dir() -> PathBuf {
        let stamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("current time")
            .as_nanos();
        std::env::temp_dir().join(format!("openprecedent-core-tests-{stamp}"))
    }

    #[test]
    fn not_implemented_uses_cli_binary_name() {
        let error = not_implemented(&["capture", "openclaw"]);
        assert_eq!(
            error.to_string(),
            "command execution is not implemented yet for openprecedent capture openclaw"
        );
    }

    #[test]
    fn parse_helpers_accept_expected_values() {
        assert_eq!(parse_output_format("json").expect("json format"), OutputFormat::Json);
        assert_eq!(parse_output_format("text").expect("text format"), OutputFormat::Text);
        assert!(parse_output_format("yaml").is_err());

        assert!(parse_bool("yes").expect("bool yes"));
        assert!(!parse_bool("off").expect("bool off"));
        assert!(parse_bool("maybe").is_err());
    }

    #[test]
    fn normalize_path_expands_home_and_relative_inputs() {
        let home = unique_temp_dir();
        fs::create_dir_all(&home).expect("create home");
        std::env::set_var("HOME", &home);

        let expanded = normalize_path(Path::new("~/runtime"), None).expect("expand home");
        assert_eq!(expanded, home.join("runtime"));

        let base = home.join("config");
        fs::create_dir_all(&base).expect("create config base");
        let relative = normalize_path(Path::new("runtime/db.sqlite"), Some(&base))
            .expect("resolve relative path");
        assert_eq!(relative, base.join("runtime/db.sqlite"));
    }

    #[test]
    fn resolve_runtime_config_uses_flag_then_env_then_default() {
        let home = unique_temp_dir();
        fs::create_dir_all(&home).expect("create home");
        std::env::set_var("HOME", &home);
        std::env::remove_var(HOME_ENV_VAR);
        std::env::remove_var(DB_ENV_VAR);
        std::env::remove_var(RUNTIME_INVOCATION_LOG_ENV_VAR);
        std::env::remove_var(COLLECTOR_STATE_ENV_VAR);
        std::env::remove_var(FORMAT_ENV_VAR);
        std::env::remove_var(NO_COLOR_ENV_VAR);

        let default_config = resolve_runtime_config(&CliConfigOverrides {
            format: None,
            no_color: false,
            home: None,
            db: None,
            invocation_log: None,
            state_file: None,
            config: None,
        })
        .expect("default config");
        assert_eq!(default_config.format.value, OutputFormat::Text);
        assert_eq!(default_config.home.path, home.join(".openprecedent").join("runtime"));

        std::env::set_var(FORMAT_ENV_VAR, "json");
        std::env::set_var(NO_COLOR_ENV_VAR, "true");
        std::env::set_var(DB_ENV_VAR, home.join("env.db"));
        let env_config = resolve_runtime_config(&CliConfigOverrides {
            format: None,
            no_color: false,
            home: None,
            db: None,
            invocation_log: None,
            state_file: None,
            config: None,
        })
        .expect("env config");
        assert_eq!(env_config.format.value, OutputFormat::Json);
        assert!(env_config.no_color.value);
        assert_eq!(env_config.db.path, home.join("env.db"));

        let flag_config = resolve_runtime_config(&CliConfigOverrides {
            format: Some(OutputFormat::Text),
            no_color: true,
            home: Some(home.join("flag-home")),
            db: Some(home.join("flag.db")),
            invocation_log: Some(home.join("flag.jsonl")),
            state_file: Some(home.join("flag-state.json")),
            config: None,
        })
        .expect("flag config");
        assert_eq!(flag_config.format.source, ConfigSource::Flag);
        assert!(flag_config.no_color.value);
        assert_eq!(flag_config.home.path, home.join("flag-home"));
        assert_eq!(flag_config.db.path, home.join("flag.db"));
    }
}
