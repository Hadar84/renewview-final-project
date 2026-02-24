"""Crew 2 — Feasibility Prediction Crew."""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class FeasibilityPredictionCrew:
    """ML pipeline: validate → features → training → evaluation + model card."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def contract_validator_agent(self) -> Agent:
        return Agent(config=self.agents_config["contract_validator_agent"], verbose=True)

    @agent
    def feature_engineering_agent(self) -> Agent:
        return Agent(config=self.agents_config["feature_engineering_agent"], verbose=True)

    @agent
    def model_training_agent(self) -> Agent:
        return Agent(config=self.agents_config["model_training_agent"], verbose=True)

    @agent
    def model_evaluation_agent(self) -> Agent:
        return Agent(config=self.agents_config["model_evaluation_agent"], verbose=True)

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
