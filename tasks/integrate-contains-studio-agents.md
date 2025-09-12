# Task: Integrate Contains Studio Specialized Agents

## Overview
Integrate the comprehensive suite of specialized AI agents from [contains-studio/agents](https://github.com/contains-studio/agents) into our Tmux Orchestrator system to enable assignment of specific roles for complete project delivery.

## Background
The Contains Studio agents repository provides 30+ specialized AI agents organized by department, each with specific expertise for rapid development workflows. These agents are designed for 6-day sprint cycles and can dramatically enhance our multi-agent orchestration capabilities.

## Available Agent Categories

### Engineering Department
- **ai-engineer** - Integrate AI/ML features that actually ship
- **backend-architect** - Design scalable APIs and server systems
- **devops-automator** - Deploy continuously without breaking things
- **frontend-developer** - Build blazing-fast user interfaces
- **mobile-app-builder** - Create native iOS/Android experiences
- **rapid-prototyper** - Build MVPs in days, not weeks
- **test-writer-fixer** - Write tests that catch real bugs

### Design Department
- **brand-guardian** - Keep visual identity consistent everywhere
- **ui-designer** - Design interfaces developers can actually build
- **ux-researcher** - Turn user insights into product improvements
- **visual-storyteller** - Create visuals that convert and share
- **whimsy-injector** - Add delight to every interaction

### Marketing Department
- **app-store-optimizer** - Dominate app store search results
- **content-creator** - Generate content across all platforms
- **growth-hacker** - Find and exploit viral growth loops
- **instagram-curator** - Master the visual content game
- **reddit-community-builder** - Win Reddit without being banned
- **tiktok-strategist** - Create shareable marketing moments
- **twitter-engager** - Ride trends to viral engagement

### Product Department
- **feedback-synthesizer** - Transform complaints into features
- **sprint-prioritizer** - Ship maximum value in 6 days
- **trend-researcher** - Identify viral opportunities

### Project Management
- **experiment-tracker** - Data-driven feature validation
- **project-shipper** - Launch products that don't crash
- **studio-producer** - Keep teams shipping, not meeting

### Studio Operations
- **analytics-reporter** - Turn data into actionable insights
- **finance-tracker** - Keep the studio profitable
- **infrastructure-maintainer** - Scale without breaking the bank
- **legal-compliance-checker** - Stay legal while moving fast
- **support-responder** - Turn angry users into advocates

### Testing & Benchmarking
- **api-tester** - Ensure APIs work under pressure
- **performance-benchmarker** - Make everything faster
- **test-results-analyzer** - Find patterns in test failures
- **tool-evaluator** - Choose tools that actually help
- **workflow-optimizer** - Eliminate workflow bottlenecks

### Bonus Agents
- **studio-coach** - Rally the AI troops to excellence (exclude **joker** as requested)

## Integration Strategy

### Phase 1: Core Framework Integration
1. **Agent Registry System**
   - Create agent role definitions compatible with tmux session management
   - Map agent capabilities to project requirements
   - Implement role assignment system for project phases

2. **Enhanced Communication Protocol**
   - Extend `send-claude-message.sh` to support role-specific messaging
   - Add agent identification and role context to communications
   - Implement role handoff mechanisms between specialized agents

3. **Role-Based Briefing System**
   - Create role-specific briefing templates
   - Integrate Contains Studio agent prompts and responsibilities
   - Implement context preservation between role switches

### Phase 2: Orchestrator Enhancement
1. **Multi-Agent Coordination**
   - Enhance `tmux_utils.py` with role management capabilities
   - Implement agent hierarchy and coordination patterns
   - Add role-specific window creation and management

2. **Project Phase Mapping**
   - Map project phases to optimal agent combinations
   - Implement automatic role suggestions based on project type
   - Create role transition workflows

3. **Quality Assurance Integration**
   - Integrate Contains Studio quality patterns
   - Implement cross-agent validation workflows
   - Add role-specific success metrics

### Phase 3: Advanced Features
1. **Dynamic Role Assignment**
   - Implement intelligent role selection based on project needs
   - Add role performance tracking and optimization
   - Create role recommendation engine

2. **Multi-Agent Workflows**
   - Design common multi-agent patterns (e.g., design → engineering → testing)
   - Implement role-based project templates
   - Add collaborative task decomposition

3. **Specialized Project Support**
   - Add support for marketing campaigns (using marketing agents)
   - Implement product launch workflows (using project-shipper + marketing)
   - Create infrastructure projects (using devops-automator + infrastructure-maintainer)

## Implementation Tasks

### 1. Agent Definition System
- [ ] Create `agents/` directory structure
- [ ] Port Contains Studio agent definitions to tmux-compatible format
- [ ] Implement agent role registry with capabilities mapping
- [ ] Create role-specific briefing templates

### 2. Enhanced Communication
- [ ] Extend communication scripts with role context
- [ ] Add role identification to message logging
- [ ] Implement role handoff protocols
- [ ] Create role-specific communication templates

### 3. Orchestrator Integration
- [ ] Add role management to TmuxOrchestrator class
- [ ] Implement role-based window creation
- [ ] Add agent coordination patterns
- [ ] Create role assignment workflow

### 4. Project Templates
- [ ] Create role-based project templates
- [ ] Implement common multi-agent workflows
- [ ] Add project type → agent mapping
- [ ] Create specialized project support

### 5. Quality & Monitoring
- [ ] Implement role performance tracking
- [ ] Add cross-agent validation
- [ ] Create role-specific success metrics
- [ ] Implement quality assurance workflows

## File Structure Changes

```
Tmux-Orchestrator/
├── agents/
│   ├── registry.py              # Agent role definitions and capabilities
│   ├── briefings/               # Role-specific briefing templates
│   │   ├── engineering/
│   │   ├── design/
│   │   ├── marketing/
│   │   ├── product/
│   │   ├── project-management/
│   │   ├── studio-operations/
│   │   └── testing/
│   └── workflows/               # Multi-agent workflow definitions
├── templates/
│   ├── projects/                # Role-based project templates
│   └── handoffs/                # Role transition templates
└── enhanced_orchestrator.py     # Role-aware orchestration system
```

## Usage Examples

### Single Role Assignment
```bash
# Assign rapid-prototyper role for MVP development
./assign-role.sh session:window rapid-prototyper "Build meditation app MVP"
```

### Multi-Agent Workflow
```bash
# Launch product development workflow
./launch-workflow.sh "fitness-app" \
  --phases "research,design,engineering,testing,marketing" \
  --agents "trend-researcher,ui-designer,rapid-prototyper,test-writer-fixer,app-store-optimizer"
```

### Role Handoff
```bash
# Handoff from design to engineering
./handoff-role.sh session:design session:engineering \
  --from ui-designer --to frontend-developer \
  --context "Design system completed, ready for implementation"
```

## Success Criteria

1. **Role Integration**: All Contains Studio agents integrated except joker
2. **Multi-Agent Coordination**: Seamless handoffs between specialized roles
3. **Project Efficiency**: Faster completion through specialized expertise
4. **Quality Improvement**: Better outcomes through role-specific validation
5. **Scalability**: System handles complex multi-agent projects effectively

## Benefits

1. **Specialized Expertise**: Each agent focuses on their domain of excellence
2. **Faster Delivery**: Parallel work by specialized agents
3. **Higher Quality**: Role-specific validation and best practices
4. **Project Flexibility**: Adapt agent teams to project requirements
5. **Knowledge Preservation**: Role-specific templates and workflows

## Risk Mitigation

1. **Complexity Management**: Gradual rollout with simple scenarios first
2. **Role Conflicts**: Clear role boundaries and handoff protocols
3. **Communication Overhead**: Efficient role-based messaging patterns
4. **Context Loss**: Robust context preservation between role switches
5. **Performance**: Monitoring and optimization of multi-agent coordination

## Next Steps

1. Review and approve integration approach
2. Begin Phase 1 implementation with core framework
3. Test with simple multi-agent scenarios
4. Gradually expand to complex workflows
5. Gather feedback and iterate on role effectiveness

This integration will transform our Tmux Orchestrator from a basic multi-agent system into a sophisticated, role-based development platform capable of handling complete project lifecycles with specialized expertise at every stage.