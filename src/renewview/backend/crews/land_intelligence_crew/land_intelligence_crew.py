"""Crew 1 — Land Intelligence Crew.

Includes a guardrail on the ingestion task to stop the crew early
if no real data was collected, and callbacks to persist task outputs.
"""

from pathlib import Path

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tasks.task_output import TaskOutput

from renewview.backend.tools.nasa_power_tool import NASAPowerTool
from renewview.backend.tools.osm_solar_tool import OSMSolarFarmTool
from renewview.backend.tools.grid_distance_tool import GridDistanceCalculatorTool
from renewview.config.settings import DATA_DIR, REPORTS_DIR


# ── Guardrail ────────────────────────────────────────────────

def _validate_ingestion_output(output: TaskOutput):
    """Guardrail: reject ingestion output that contains no real data.

    Checks that the agent actually collected data rather than reporting
    an error. If rejected, the agent retries. After guardrail_max_retries
    exhausted the crew stops with a clear error.
    """
    raw = output.raw if hasattr(output, "raw") else str(output)

    has_coords = "latitude" in raw.lower() and "longitude" in raw.lower()

    failure_phrases = [
        "no data", "could not", "unable to", "not possible",
        "no csv", "no solar farm data", "failed to",
    ]
    is_failure = any(phrase in raw.lower() for phrase in failure_phrases)

    data_lines = sum(
        1 for line in raw.split("\n")
        if "," in line and any(c.isdigit() for c in line)
    )

    if not has_coords or (is_failure and data_lines < 10):
        return (
            False,
            "REJECTED: Output contains no valid data. You MUST call the "
            "nasa_power_solar_data tool and osm_solar_farms tool to collect "
            "real data points across PT, ES, GR, IT. If an API call fails, "
            "retry it. Your final output MUST be CSV rows with latitude, "
            "longitude, ghi, and other climate columns.",
        )

    return (True, output)


# ── File-saving callbacks ────────────────────────────────────

def _make_save_callback(file_path: Path):
    """Create a callback that writes task output to a file."""
    def _save(output: TaskOutput) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        raw = output.raw if hasattr(output, "raw") else str(output)
        file_path.write_text(raw, encoding="utf-8")
        print(f"  >> Saved {file_path.name} ({len(raw):,} chars)")
    return _save


# ── Crew ─────────────────────────────────────────────────────

@CrewBase
class LandIntelligenceCrew:
    """Data pipeline: ingestion → cleaning → EDA → contract."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def data_ingestion_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["data_ingestion_agent"],
            tools=[NASAPowerTool(), OSMSolarFarmTool(), GridDistanceCalculatorTool()],
            verbose=True,
        )

    @agent
    def data_cleaning_agent(self) -> Agent:
        return Agent(config=self.agents_config["data_cleaning_agent"], verbose=True)

    @agent
    def eda_agent(self) -> Agent:
        return Agent(config=self.agents_config["eda_agent"], verbose=True)

    @agent
    def dataset_contract_agent(self) -> Agent:
        return Agent(config=self.agents_config["dataset_contract_agent"], verbose=True)

    @task
    def data_ingestion_task(self) -> Task:
        return Task(
            config=self.tasks_config["data_ingestion_task"],
            guardrail=_validate_ingestion_output,
            guardrail_max_retries=2,
            callback=_make_save_callback(DATA_DIR / "raw_solar_data.csv"),
        )

    @task
    def data_cleaning_task(self) -> Task:
        return Task(
            config=self.tasks_config["data_cleaning_task"],
            callback=_make_save_callback(DATA_DIR / "clean_solar_data.csv"),
        )

    @task
    def eda_task(self) -> Task:
        return Task(
            config=self.tasks_config["eda_task"],
            callback=_make_save_callback(REPORTS_DIR / "eda_report.md"),
        )

    @task
    def dataset_contract_task(self) -> Task:
        return Task(
            config=self.tasks_config["dataset_contract_task"],
            callback=_make_save_callback(DATA_DIR / "dataset_contract.json"),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, tasks=self.tasks,
            process=Process.sequential, verbose=True,
        )
