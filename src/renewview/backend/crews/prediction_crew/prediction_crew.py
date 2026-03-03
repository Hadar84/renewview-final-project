"""Crew 2 — Feasibility Prediction Crew."""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from renewview.backend.tools.contract_validation_tool import ContractValidationTool
from renewview.backend.tools.feature_engineering_tool import FeatureEngineeringTool
from renewview.backend.tools.model_evaluation_tool import ModelEvaluationTool
from renewview.backend.tools.model_training_tool import ModelTrainingTool


@CrewBase
class FeasibilityPredictionCrew:
    """ML pipeline: validate → features → training → evaluation + model card."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def contract_validator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["contract_validator_agent"],
            tools=[ContractValidationTool()],
            verbose=True,
        )

    @agent
    def feature_engineering_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["feature_engineering_agent"],
            tools=[FeatureEngineeringTool()],
            verbose=True,
        )

    @agent
    def model_training_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["model_training_agent"],
            tools=[ModelTrainingTool()],
            verbose=True,
        )

    @agent
    def model_evaluation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["model_evaluation_agent"],
            tools=[ModelEvaluationTool()],
            verbose=True,
        )

    @task
    def contract_validation_task(self) -> Task:
        return Task(config=self.tasks_config["contract_validation_task"])

    @task
    def feature_engineering_task(self) -> Task:
        return Task(config=self.tasks_config["feature_engineering_task"])

    @task
    def model_training_task(self) -> Task:
        return Task(config=self.tasks_config["model_training_task"])

    @task
    def model_evaluation_task(self) -> Task:
        return Task(config=self.tasks_config["model_evaluation_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, tasks=self.tasks,
            process=Process.sequential, verbose=True,
        )
