#!/usr/bin/env python3
"""
GitHub Spec Kit Integration for Tmux Orchestrator
Implements Specification-Driven Development (SDD) for autonomous agent task creation

This module adapts the GitHub Spec Kit methodology for the Tmux Orchestrator's
autonomous multi-agent development environment.

Core Concepts from Spec Kit:
- /specify: Create feature specifications from natural language
- /plan: Generate technical implementation plans
- /tasks: Break down plans into executable, dependency-ordered tasks
- Templates: Structured templates enforce quality and completeness
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class SpecKitIntegration:
    """
    Integrates GitHub Spec Kit methodology into Tmux Orchestrator
    for structured, specification-driven agent task creation.
    """

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.specs_dir = self.project_path / "specs"
        self.templates_dir = self.project_path / "spec-kit-templates"
        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directory structure for Spec Kit integration"""
        self.specs_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)

        # Create memory directory for constitutional guidelines
        memory_dir = self.project_path / "memory"
        memory_dir.mkdir(exist_ok=True)

    def get_next_feature_number(self) -> str:
        """
        Get the next sequential feature number by scanning existing specs
        Returns format: "001", "002", etc.
        """
        existing_features = []
        if self.specs_dir.exists():
            for item in self.specs_dir.iterdir():
                if item.is_dir() and item.name[:3].isdigit():
                    existing_features.append(int(item.name[:3]))

        next_num = max(existing_features, default=0) + 1
        return f"{next_num:03d}"

    def create_feature_branch_name(self, description: str) -> str:
        """
        Create semantic branch name from feature description
        Example: "Real-time chat system" -> "003-realtime-chat-system"
        """
        feature_num = self.get_next_feature_number()

        # Convert description to branch-safe format
        clean_desc = description.lower()
        clean_desc = "".join(c if c.isalnum() or c.isspace() else "" for c in clean_desc)
        clean_desc = "-".join(clean_desc.split())[:40]  # Limit length

        return f"{feature_num}-{clean_desc}"

    def specify_command(self, feature_description: str) -> Dict[str, str]:
        """
        Implement /specify command: Create feature specification from natural language

        This mirrors the GitHub Spec Kit /specify command but adapted for agent workflows:
        1. Generate feature number and branch name
        2. Create feature specification using template
        3. Return paths and metadata for agent use
        """
        branch_name = self.create_feature_branch_name(feature_description)
        feature_dir = self.specs_dir / branch_name
        feature_dir.mkdir(exist_ok=True)

        spec_file = feature_dir / "spec.md"

        # Generate specification using template
        spec_content = self._generate_feature_spec(
            feature_description,
            branch_name,
            datetime.now().strftime('%Y-%m-%d')
        )

        spec_file.write_text(spec_content)

        logger.info(f"Created feature specification: {spec_file}")

        return {
            'branch_name': branch_name,
            'feature_dir': str(feature_dir),
            'spec_file': str(spec_file),
            'feature_number': branch_name[:3],
            'status': 'specification_created'
        }

    def plan_command(self, branch_name: str, technical_details: str) -> Dict[str, str]:
        """
        Implement /plan command: Generate technical implementation plan

        Reads the feature specification and creates:
        1. Implementation plan (plan.md)
        2. Research document (research.md)
        3. Data model (data-model.md) if applicable
        4. API contracts (contracts/) if applicable
        5. Quickstart guide (quickstart.md)
        """
        feature_dir = self.specs_dir / branch_name
        if not feature_dir.exists():
            raise ValueError(f"Feature directory not found: {feature_dir}")

        spec_file = feature_dir / "spec.md"
        if not spec_file.exists():
            raise ValueError(f"Specification file not found: {spec_file}")

        # Read specification to understand requirements
        spec_content = spec_file.read_text()

        # Generate implementation plan
        plan_file = feature_dir / "plan.md"
        plan_content = self._generate_implementation_plan(
            spec_content,
            technical_details,
            branch_name,
            datetime.now().strftime('%Y-%m-%d')
        )
        plan_file.write_text(plan_content)

        # Generate supporting documents
        research_file = feature_dir / "research.md"
        research_content = self._generate_research_doc(technical_details, branch_name)
        research_file.write_text(research_content)

        # Create contracts directory if API endpoints are involved
        if "api" in technical_details.lower() or "endpoint" in technical_details.lower():
            contracts_dir = feature_dir / "contracts"
            contracts_dir.mkdir(exist_ok=True)

        logger.info(f"Created implementation plan: {plan_file}")

        return {
            'branch_name': branch_name,
            'feature_dir': str(feature_dir),
            'plan_file': str(plan_file),
            'research_file': str(research_file),
            'status': 'plan_created'
        }

    def tasks_command(self, branch_name: str) -> Dict[str, str]:
        """
        Implement /tasks command: Generate executable, dependency-ordered tasks

        Analyzes the implementation plan and supporting documents to create:
        1. Numbered, sequential tasks (T001, T002, ...)
        2. Parallel execution markers [P] for independent tasks
        3. Dependency ordering (tests before implementation)
        4. Specific file paths for each task
        """
        feature_dir = self.specs_dir / branch_name
        if not feature_dir.exists():
            raise ValueError(f"Feature directory not found: {feature_dir}")

        plan_file = feature_dir / "plan.md"
        if not plan_file.exists():
            raise ValueError(f"Implementation plan not found: {plan_file}")

        # Read implementation plan
        plan_content = plan_file.read_text()

        # Read supporting documents if they exist
        supporting_docs = {}
        for doc_name in ['research.md', 'data-model.md', 'quickstart.md']:
            doc_file = feature_dir / doc_name
            if doc_file.exists():
                supporting_docs[doc_name] = doc_file.read_text()

        # Check for contracts directory
        contracts_dir = feature_dir / "contracts"
        if contracts_dir.exists():
            supporting_docs['contracts'] = [f.name for f in contracts_dir.iterdir()]

        # Generate tasks
        tasks_file = feature_dir / "tasks.md"
        tasks_content = self._generate_tasks(
            plan_content,
            supporting_docs,
            branch_name,
            datetime.now().strftime('%Y-%m-%d')
        )
        tasks_file.write_text(tasks_content)

        logger.info(f"Created tasks breakdown: {tasks_file}")

        return {
            'branch_name': branch_name,
            'feature_dir': str(feature_dir),
            'tasks_file': str(tasks_file),
            'status': 'tasks_created'
        }

    def _generate_feature_spec(self, description: str, branch_name: str, date: str) -> str:
        """Generate feature specification content using Spec Kit template patterns"""

        # Extract key concepts from description
        key_concepts = self._extract_key_concepts(description)

        return f"""# Feature Specification: {key_concepts['feature_name']}

**Feature Branch**: `{branch_name}`
**Created**: {date}
**Status**: Draft
**Input**: User description: "{description}"

## Execution Flow (main)
```
1. Parse user description from Input
   → Extract key concepts: {', '.join(key_concepts['concepts'])}
2. Generate User Scenarios based on description
3. Create Functional Requirements (FR-001, FR-002, ...)
4. Identify Key Entities if data is involved
5. Mark unclear aspects with [NEEDS CLARIFICATION: specific question]
6. Run Review Checklist
7. Return: SUCCESS (spec ready for planning)
```

## User Scenarios & Testing *(mandatory)*

### Primary User Stories
{self._generate_user_stories(description, key_concepts)}

### Acceptance Criteria
{self._generate_acceptance_criteria(description)}

## Requirements *(mandatory)*

### Functional Requirements
{self._generate_functional_requirements(description)}

### Key Entities *(include if feature involves data)*
{self._generate_key_entities(description)}

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [x] User description parsed
- [x] Key concepts extracted
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [x] Review checklist created

---

*Generated by Tmux Orchestrator Spec Kit Integration*
"""

    def _generate_implementation_plan(self, spec_content: str, technical_details: str, branch_name: str, date: str) -> str:
        """Generate implementation plan content"""

        return f"""# Implementation Plan: {branch_name}

**Branch**: `{branch_name}` | **Date**: {date} | **Spec**: spec.md
**Input**: Feature specification + Technical details: "{technical_details}"

## Execution Flow (/plan command scope)
```
1. Read feature specification requirements
2. Apply technical constraints: {technical_details}
3. Generate project structure
4. Create Phase 0: Research
5. Create Phase 1: Design & Contracts
6. Document task planning approach for /tasks command
7. Return: SUCCESS (ready for /tasks)
```

## Summary

This implementation plan translates the feature specification into a concrete technical approach using:
{self._extract_tech_stack(technical_details)}

## Technical Context

### Technology Stack
{self._generate_tech_stack_details(technical_details)}

### Architecture Decisions
{self._generate_architecture_decisions(technical_details)}

## Project Structure

### Documentation (this feature)
```
specs/{branch_name}/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

## Phase 0: Research & Setup

### Technology Research
- Evaluate {self._extract_primary_tech(technical_details)} for this use case
- Identify required dependencies and tools
- Research best practices and patterns

## Phase 1: Design & Contracts

### API Design (if applicable)
- Define REST endpoints or communication interfaces
- Document request/response schemas
- Create contract tests

### Data Model Design (if applicable)
- Identify core entities and relationships
- Define data persistence strategy
- Plan migration approach

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load templates/tasks-template.md as base
- Generate tasks from Phase 1 design docs
- Each contract → contract test task [P]
- Each entity → model creation task [P]
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

---

*Generated by Tmux Orchestrator Spec Kit Integration*
"""

    def _generate_tasks(self, plan_content: str, supporting_docs: Dict, branch_name: str, date: str) -> str:
        """Generate tasks breakdown content"""

        feature_name = branch_name.replace('-', ' ').title()

        return f"""# Tasks: {feature_name}

**Input**: Design documents from `/specs/{branch_name}/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md and extract tech stack, libraries, structure
2. Load supporting documents: {', '.join(supporting_docs.keys())}
3. Generate tasks by category: Setup → Tests → Core → Integration → Polish
4. Apply task rules: Different files = [P], Same file = sequential
5. Number tasks sequentially (T001, T002...)
6. Create dependency graph and parallel execution examples
7. Validate task completeness
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Phase 3.1: Setup
- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize project with dependencies from research.md
- [ ] T003 [P] Configure development environment and tools

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
{self._generate_test_tasks(supporting_docs)}

## Phase 3.3: Core Implementation (ONLY after tests are failing)
{self._generate_implementation_tasks(plan_content, supporting_docs)}

## Phase 3.4: Integration
{self._generate_integration_tasks(supporting_docs)}

## Phase 3.5: Polish
- [ ] T020 [P] Add comprehensive error handling
- [ ] T021 [P] Implement logging and monitoring
- [ ] T022 [P] Add performance optimizations
- [ ] T023 [P] Create documentation and examples

## Dependencies
- Tests (T004-T010) before implementation (T011-T017)
- Setup tasks (T001-T003) before all others
- Integration tasks (T018-T019) after core implementation

## Parallel Example
```
# Launch T004-T006 together (different test files):
Task: "Create unit tests for core entities in tests/unit/test_entities.py"
Task: "Create integration tests for API endpoints in tests/integration/test_api.py"
Task: "Create contract tests for external services in tests/contract/test_external.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

---

*Generated by Tmux Orchestrator Spec Kit Integration*
"""

    # Helper methods for content generation
    def _extract_key_concepts(self, description: str) -> Dict[str, any]:
        """Extract key concepts from feature description"""
        # Simple keyword extraction - could be enhanced with NLP
        concepts = []
        if "user" in description.lower():
            concepts.append("user management")
        if "data" in description.lower() or "store" in description.lower():
            concepts.append("data persistence")
        if "api" in description.lower() or "endpoint" in description.lower():
            concepts.append("API interface")
        if "ui" in description.lower() or "interface" in description.lower():
            concepts.append("user interface")

        # Extract feature name from description (first few words)
        words = description.split()[:4]
        feature_name = " ".join(words).title()

        return {
            'feature_name': feature_name,
            'concepts': concepts
        }

    def _generate_user_stories(self, description: str, key_concepts: Dict) -> str:
        """Generate user stories from description"""
        return f"""
**US-001**: As a user, I want to {description.lower()[:100]}...
**US-002**: As a system administrator, I want to manage and monitor the feature
**US-003**: As a developer, I want clear APIs and documentation for integration
"""

    def _generate_acceptance_criteria(self, description: str) -> str:
        """Generate acceptance criteria"""
        return f"""
**AC-001**: System successfully processes user requests without errors
**AC-002**: All user interactions complete within acceptable time limits
**AC-003**: Data integrity is maintained throughout all operations
**AC-004**: Error conditions are handled gracefully with clear messaging
"""

    def _generate_functional_requirements(self, description: str) -> str:
        """Generate functional requirements"""
        return f"""
**FR-001**: System MUST implement core functionality as described: {description[:200]}...
**FR-002**: System MUST validate all user inputs and provide appropriate feedback
**FR-003**: System MUST maintain data consistency and integrity
**FR-004**: System MUST handle error conditions gracefully
**FR-005**: System MUST provide logging for audit and debugging purposes
"""

    def _generate_key_entities(self, description: str) -> str:
        """Generate key entities if data is involved"""
        if "data" in description.lower() or "user" in description.lower():
            return """
**User**: Represents system users with authentication and permissions
**Session**: Manages user authentication and activity tracking
**AuditLog**: Records system events for compliance and debugging
"""
        return "No data entities identified for this feature."

    def _extract_tech_stack(self, technical_details: str) -> str:
        """Extract technology stack from technical details"""
        # Simple extraction - could be enhanced
        return f"- {technical_details[:100]}..."

    def _generate_tech_stack_details(self, technical_details: str) -> str:
        """Generate detailed technology stack information"""
        return f"""
### Primary Technologies
{technical_details}

### Development Tools
- Testing framework for unit and integration tests
- Linting and code formatting tools
- Build and deployment automation
"""

    def _generate_architecture_decisions(self, technical_details: str) -> str:
        """Generate architecture decisions"""
        return f"""
### Key Decisions
1. **Technology Choice**: {technical_details[:50]}...
2. **Testing Strategy**: Test-driven development with comprehensive coverage
3. **Error Handling**: Graceful degradation with comprehensive logging
4. **Code Organization**: Modular structure with clear separation of concerns
"""

    def _extract_primary_tech(self, technical_details: str) -> str:
        """Extract primary technology from technical details"""
        words = technical_details.split()[:3]
        return " ".join(words)

    def _generate_research_doc(self, technical_details: str, branch_name: str) -> str:
        """Generate research document content"""
        return f"""# Research Document: {branch_name}

## Technology Research

### Primary Technologies
{technical_details}

### Research Questions
1. What are the best practices for implementing this technology stack?
2. What are the performance implications of the chosen approach?
3. What are the potential scalability challenges?
4. What security considerations need to be addressed?

### Implementation Recommendations
Based on the technical requirements: {technical_details}

### Dependencies and Tools
- Core frameworks and libraries needed
- Development and testing tools
- Deployment and monitoring requirements

---

*Generated by Tmux Orchestrator Spec Kit Integration*
"""

    def _generate_test_tasks(self, supporting_docs: Dict) -> str:
        """Generate test-related tasks"""
        tasks = []
        task_num = 4

        if 'contracts' in supporting_docs:
            for contract in supporting_docs['contracts']:
                tasks.append(f"- [ ] T{task_num:03d} [P] Create contract tests for {contract}")
                task_num += 1

        tasks.extend([
            f"- [ ] T{task_num:03d} [P] Create unit tests for core functionality",
            f"- [ ] T{task_num+1:03d} [P] Create integration tests for main workflows",
            f"- [ ] T{task_num+2:03d} [P] Create end-to-end tests for user scenarios"
        ])

        return "\n".join(tasks)

    def _generate_implementation_tasks(self, plan_content: str, supporting_docs: Dict) -> str:
        """Generate implementation tasks"""
        return """
- [ ] T011 Implement core data models and entities
- [ ] T012 [P] Implement business logic and service layer
- [ ] T013 [P] Implement API endpoints or interfaces
- [ ] T014 [P] Implement user interface components
- [ ] T015 Implement main workflow coordination
- [ ] T016 [P] Implement validation and error handling
- [ ] T017 [P] Implement data persistence layer
"""

    def _generate_integration_tasks(self, supporting_docs: Dict) -> str:
        """Generate integration tasks"""
        return """
- [ ] T018 Integrate all components and test system workflows
- [ ] T019 [P] Configure deployment and environment setup
"""

# Integration with existing Tmux Orchestrator systems
class TmuxSpecKitAgent:
    """
    Agent wrapper that enables autonomous agents to use Spec Kit methodology
    for structured task creation and execution.
    """

    def __init__(self, project_path: Path, agent_name: str):
        self.spec_kit = SpecKitIntegration(project_path)
        self.agent_name = agent_name
        self.current_feature = None

    def start_new_feature(self, description: str) -> Dict[str, str]:
        """Agent command: Start new feature using /specify"""
        result = self.spec_kit.specify_command(description)
        self.current_feature = result['branch_name']
        self.log_agent_activity(f"Started feature: {result['branch_name']}")
        return result

    def create_implementation_plan(self, technical_details: str) -> Dict[str, str]:
        """Agent command: Create implementation plan using /plan"""
        if not self.current_feature:
            raise ValueError("No active feature. Use start_new_feature() first.")

        result = self.spec_kit.plan_command(self.current_feature, technical_details)
        self.log_agent_activity(f"Created implementation plan for: {self.current_feature}")
        return result

    def generate_tasks(self) -> Dict[str, str]:
        """Agent command: Generate executable tasks using /tasks"""
        if not self.current_feature:
            raise ValueError("No active feature. Use start_new_feature() first.")

        result = self.spec_kit.tasks_command(self.current_feature)
        self.log_agent_activity(f"Generated tasks for: {self.current_feature}")
        return result

    def log_agent_activity(self, message: str):
        """Log agent activity for debugging and monitoring"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"[{timestamp}] {self.agent_name}: {message}")

if __name__ == "__main__":
    # Example usage
    project_path = Path("/example/project")

    # Initialize Spec Kit integration
    spec_kit = SpecKitIntegration(project_path)

    # Create a new feature specification
    result = spec_kit.specify_command("Real-time chat system with message history")
    print(f"Created specification: {result}")

    # Generate implementation plan
    plan_result = spec_kit.plan_command(
        result['branch_name'],
        "WebSocket for real-time messaging, PostgreSQL for history, Redis for presence"
    )
    print(f"Created plan: {plan_result}")

    # Generate executable tasks
    tasks_result = spec_kit.tasks_command(result['branch_name'])
    print(f"Created tasks: {tasks_result}")