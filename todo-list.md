# TODO roadmap v0.0.1+beta

## Phase 1

- [ ] Complete initial project setup and environment configuration
- [ ] Deploy and implement core project architecture (folders, modules, agents, layers)
- [ ] Develop basic agent framework and communication protocols
- [ ] Create testing infrastructure and validation suite
- [ ] Document current phase progress and next steps

- [ ] Dynamic agent registration
- [ ] Centralized task delegation
- [ ] Agent-to-agent communication (via message bus)
- [ ] Execution pipeline (task assignment → agent reasoning → result collection)

- [ ] Receives a task from the human or workflow.
- [ ] Calls the PlannerAgent → produces a structured plan.
- [ ] Sends subtasks to DeveloperAgent.
- [ ] Passes results to ReviewAgent for validation.
- [ ] Returns a summarized report to the workflow/human.
- (Data Flows) Human/Workflow → TaskManager → PlannerAgent → DeveloperAgent → ReviewAgent → Output

- [ ] Agents to remember previous context, plans, and results.
- [ ] The system to validate or auto-approve each step before proceeding.
- [ ] Fully compatible with free, local, lightweight setup (no paid DBs or APIs).

- [ ] Allow multiple agents to work concurrently on independent subtasks.
- [ ] Introduce task queuing & prioritization for Planner → Developer → Reviewer.
- [ ] Use asyncio and in-memory MessageBus for coordination.
- [ ] Keep free tooling only — Python built-ins, asyncio, no paid APIs.
- [ ] Maintain memory & approval for every agent step.
