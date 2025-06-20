# PyDataStudio

PyDataStudio is a Python framework built on Pandas, designed to streamline and automate data analysis workflows and collaborative report generation. It employs a modular structure, allowing users to define 'studies' (or researches) that process data and produce outputs, primarily Excel reports. The framework is highly configurable through YAML files, enabling flexible data manipulation, filtering, and reporting tailored to specific needs.

## Features

- **Pandas-Powered Data Manipulation:**
    - Core operations leverage Pandas DataFrames for efficient data handling.
    - Load data directly from Excel sheets into DataFrames.
- **Advanced Data Filtering:**
    - Filter DataFrames using another DataFrame as a criteria.
    - Sophisticated dictionary-based filtering (`data_filter_by_dict`, `DataFrameManager.obtain_filtered_data`) supporting:
        - AND/OR logic for multiple conditions.
        - Regular expressions for pattern matching.
        - Comparison operators (`<`, `>`, `=`).
        - Custom callable functions for complex filtering logic.
- **Structured Query Management (`DataframeQueryManager`):**
    - Define and manage complex data filtering strategies using YAML configuration.
    - Apply general (default) filters based on scopes (regex matching against goal/element names).
    - Implement goal-specific pre-filters and element-specific overrides.
- **Configuration-Driven Environment (`pydatastudio.environment`):**
    - Manage multiple operational environments (e.g., development, test, production) through YAML files.
    - Dynamically resolve configuration values using a `ContextManager`, allowing placeholders in configuration strings to be filled at runtime.
    - Singleton pattern for environment-aware objects ensures consistent configuration access.
- **Automated Excel Report Generation (`BasicExcelEditor`):**
    - Save analysis results (DataFrames) to structured Excel files.
    - Highly configurable output:
        - Dynamic file paths and sheet names using context variables (e.g., dates, group names).
        - Pre-filtering data before saving to Excel.
        - Organization of data into multiple sheets and potentially hierarchical structures based on configuration.
    - Asynchronous file saving using threading to improve performance.
- **Orchestration with `DataStudio`:**
    - (Conceptual) The `DataStudio` class appears to orchestrate 'researches' (studies), managing the execution of analysis tasks and their outputs.
- **Utility Modules:**
    - `resourcesmanager`: Robustly resolve and manage paths to project resources, handling frozen application scenarios.
    - `Logging`: Centralized and configurable logging based on Python's standard `logging` module.
    - `CaseFormatter`: Extended string formatting with custom conversion flags (e.g., `!u` for uppercase, `!l` for lowercase, `!c` for capitalize).
- **(Optional) Web Interaction:**
    - Includes a `driverfactory` for creating Selenium WebDriver instances (Chrome, Firefox), suggesting capabilities for web scraping as a potential data source.

## Getting Started

### Prerequisites

*   Python 3.7+ (recommended, due to f-string usage and modern features)
*   Pandas
*   PyYAML (for YAML configuration files)
*   openpyxl (for reading and writing Excel files)
*   (Optional) Selenium (if using `driverfactory` for web automation)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd PyDataStudio/pydatastudio
    ```
    (Assuming `readme.md` and the project root are in `PyDataStudio/pydatastudio`)

2.  **Install dependencies:**
    Create a virtual environment (recommended):
    ```bash
    python -m venv .venv
    # On Windows
    .\.venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```
    Install the required packages:
    ```bash
    pip install pandas pyyaml openpyxl
    # If using web scraping features:
    # pip install selenium
    ```

### Configuration

PyDataStudio relies heavily on YAML configuration files for its operations.

*   **Environment Configuration:**
    -   Managed by `pydatastudio.environment.environmentconfigmanagement`.
    -   Typically, you'll have a main YAML file defining different environments (e.g., `Test`, `Production`).
    -   The structure includes a `config_name` (often the filename), a `Current` key specifying the active environment, and then separate sections for each defined environment.
    -   Example:
        ```yaml
        config_name: "my_project_config"
        Current: "Development"

        Development:
          reports_path: "./output/dev/"
          database_url: "dev_db_connection_string"
          # ... other dev-specific settings

        Production:
          reports_path: "/srv/reports/prod/"
          database_url: "prod_db_connection_string"
          # ... other prod-specific settings
        ```
    -   Load configurations using `environmentconfigmanagement.get_environment_config_by_yaml_file("path/to/your/config.yaml")`.
*   **Logging Configuration:**
    -   The `pydatastudio.logging` module is configured via a `logging.conf` file (by default, expected in `./conf/logging.conf` relative to where `resourcesmanager` determines the base path).
*   **Query Configuration (`DataframeQueryManager`):**
    -   Define complex filtering logic in YAML files. These specify `general` filters (with scopes) and `detail` sections for specific `goals` and `elements`.

### Basic Workflow (Conceptual)

1.  **Define Configurations:**
    *   Set up your environment(s) in a master YAML configuration file.
    *   Create YAML files for `DataframeQueryManager` if using structured queries.
    *   Configure `logging.conf`.
2.  **Initialize Environment:**
    *   Load the environment configuration using `pydatastudio.environment.environmentconfigmanagement`.
    *   Create a `BaseEnvironmentObject` instance, passing the loaded configuration parser.
3.  **Manage Context (Optional):**
    *   Use `pydatastudio.environment.contextmanager.ContextManager` to set and get runtime variables that can be used to format configuration strings (e.g., dates for file paths).
4.  **Load Data:**
    *   Use `pydatastudio.data.dataframeutils.obtain_dataframe_from_sheet` or `pydatastudio.data.dataframemanager.DataFrameManager` to load data (e.g., from Excel) into Pandas DataFrames.
5.  **Process Data:**
    *   Apply filters using `DataframeQueryManager` by loading its YAML configuration.
    *   Alternatively, use `pydatastudio.data.dataframeutils.data_filter_by_dict` or `DataFrameManager.obtain_filtered_data` for direct filtering.
    *   Perform necessary data transformations and analyses using Pandas.
6.  **Generate Reports:**
    *   Utilize `pydatastudio.data.studio.editors.basicexceleditor.BasicExcelEditor` (likely orchestrated through a `DataStudio` instance) to save processed DataFrames to Excel. The editor's behavior (output paths, sheet names, pre-save filters) is driven by its own section within the environment configuration.

## Core Components

*   **`pydatastudio.data`**: Contains modules for core data operations.
    *   `dataframeutils.py`: Standalone utility functions for Pandas DataFrame manipulation (filtering, merging).
    *   `dataframemanager.py`: A class-based wrapper for DataFrames, offering filtering and utility methods.
    *   `dataframequerymanager.py`: Manages complex, reusable filter definitions from YAML configurations.
    *   `studio/`: Likely houses higher-level components for orchestrating data studies.
        *   `editors/basicexceleditor.py`: Responsible for writing DataFrames to Excel files based on configuration.
        *   `datastudio.py`: (Inferred) A central class for managing and executing "researches" or studies.
*   **`pydatastudio.environment`**: Manages the application's configuration and runtime context.
    *   `environmentconfig.py` & `environmentconfigmanagement.py`: Handle loading, parsing, and accessing hierarchical YAML-based configurations for different environments.
    *   `contextmanager.py`: Provides a global context for sharing data and dynamically resolving configuration strings.
    *   `baseenvironment.py`: A base class for objects that need to be aware of and use the application's environment configuration and context.
*   **`pydatastudio.utils`** (Conceptual grouping for standalone utilities):
    *   `caseformatter.py`: Extends Python's string formatting with custom case conversions.
    *   `logging.py`: Provides a simple interface to a pre-configured logging system.
    *   `resourcesmanager.py`: Helps in resolving file paths to resources within the project.
*   **`pydatastudio.driverfactory`**: (Optional) Provides a factory for Selenium WebDriver instances, for web automation tasks.

## Running Tests

The project uses Python's `unittest` framework. Tests can typically be run from the project's root directory (e.g., `PyDataStudio/` or `PyDataStudio/pydatastudio/` depending on structure):

```bash
python -m unittest discover -s test
```
Or by running individual test files:
```bash
python -m unittest test.pydatastudio.data.testDataframeUtils
```
