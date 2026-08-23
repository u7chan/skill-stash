---
name: language-teacher-template
description: Use when creating or improving a teacher/mentor skill for a programming language. Design it to teach language-specific mental models, comparisons, error explanations, review criteria, and practical judgment, not a catalog of syntax.
---

# Language Teacher Template

Design a teacher skill that teaches a programming language through **how to think**, not how to write it.

The finished skill should leave learners able to do the following on their own:

- Predict what code does before running it
- Explain why the compiler / runtime behaves that way
- Pick the language-idiomatic option among similar choices
- Understand errors well enough to prevent recurrence, not just patch them locally
- Judge real-world code by correctness / idiom / simplicity

Do not turn it into a syntax cheat sheet, an API index, or a giant list of best practices.

## 1. Define the Design Inputs

For the target language, identify at least the following:

- **Target**: whether the main audience is beginners, developers coming from other languages, or production users
- **Core mental models**: concepts that are indispensable for predicting behavior
- **Common traps**: points where intuition from other languages leads people astray
- **Decision pairs**: pairs where you must explain when to choose A vs B
- **Error model**: how compile errors / runtime errors / exceptions or error values are handled
- **Concurrency / resource model**: concurrency, ownership, lifecycle, and disposal responsibility
- **Tooling**: formatter, tests, lint/static analysis, debugger, race/fuzz tools, etc.

Extract "what you need to think about in this language and how" before fine-grained syntax.

## 2. Core Teaching Flow

Explanations normally follow this order:

1. **Conclusion** — answer briefly first
2. **Minimal example** — a small snippet that shows only the concept
3. **What happens** — how values, types, memory, and control flow behave
4. **Why it happens** — the language-specific mental model
5. **Common mistakes** — include misunderstandings carried over from other languages
6. **How to choose** — the practical decision criteria
7. **Go deeper** — only when needed, move on to internals or advanced examples

Do not explain everything up front. Use progressive disclosure matched to the depth of the question.

## 3. Mental Model First

For each important concept, make sure you can answer at least these questions:

- **Who owns** this value / object / resource?
- On assignment or argument passing, **what is copied and what is shared**?
- What does the type system **guarantee, and what does it not guarantee**?
- In what form do **failures reach the caller**?
- Once concurrency is started, **who is responsible for finishing, waiting, and cancellation**?
- **When** should an abstraction be introduced?
- What does the zero/default/null/nil equivalent value **mean**?

Do not force concepts the language does not have. Replace them with the questions that matter for that language.

## 4. Comparison Rule

Do not stop at explaining the "differences" in a comparison.

For every comparison, always cover:

- What each side represents
- The runtime / type-system difference
- Which one is the default
- Under what conditions to choose the other side
- What problems tend to occur when it is misused

Example:

```text
A vs B
- Mental model:
- Default:
- Choose A when:
- Choose B when:
- Common mistake:
```

## 5. Error Explanation

When asked about an error, do not reply with only the fixed code.

Explain in this order:

1. **What happened**
2. **Why the language implementation rejected / failed**
3. **The smallest part that is the problem**
4. **The minimal fix**
5. **A more idiomatic way** (when there is a difference)
6. **A rule for spotting the same kind of problem**

Teach the causal model, not memorization of error message wording.

## 6. Review Mode

In code review, organize findings along these axes:

- **correctness**: are behavior, types, and boundary conditions right?
- **language model**: does it misunderstand the language's value / type / resource model?
- **idiom**: is it a natural expression in that language?
- **lifecycle / concurrency**: are responsibilities for leaks, races, cancellation, and cleanup clear?
- **error semantics**: are propagation, classification, and context for failures appropriate?
- **simplicity**: is abstraction or framework-building getting ahead of the problem?

Do not treat "making it more advanced" as improvement. If it is correct and simple, keep it.

## 7. Example Rule

Keep examples small and let each one explain a single concept.

- Do not drag in unrelated frameworks or libraries
- Do not add error handling that is irrelevant to the point
- When showing Bad / Better, state what the change improves
- Cover advanced optimizations only when measurements or requirements call for them

## 8. Reference Split

Keep only the teaching judgment rules in `SKILL.md`.

Split out language-specific details when needed.

```text
<language>-teacher/
├── SKILL.md
└── references/
    ├── mental-models.md
    ├── patterns.md
    └── tooling.md
```

- `mental-models.md`: values, types, memory, errors, concurrency, etc.
- `patterns.md`: comparisons, typical mistakes, Before/After
- `tooling.md`: formatter, tests, static analysis, debugging, etc.

For small language skills, do not add files; split only when the need arises.

See [references/skeleton.md](references/skeleton.md) for a concrete skeleton.

## 9. Source Rule

Treat the language specification and official documentation as primary sources.

- For version-dependent behavior, check the current target version
- Use blog posts and community articles only as supplementary material
- Do not confuse "well-known best practices" with the specification
- Do not assert old idioms as the current standard

## Final Check

Verify before considering a teacher skill finished:

- Mental models are at the center, not a syntax catalog
- Important comparisons say "when to choose which"
- Error explanations run cause → fix → recurrence prevention
- Reviews do not push toward over-engineering
- Language-specific details do not crowd `SKILL.md`
- Official sources and version-dependent facts are kept apart
- The goal is that learners eventually judge on their own
