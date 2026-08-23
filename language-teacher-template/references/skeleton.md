# Language Teacher Skill Skeleton

A starting skeleton for building a language-specific teacher skill.

Do not fill it in mechanically; keep only the concepts that truly matter for the target language.

## SKILL.md

```md
---
name: <language>-teacher
description: Use for learning, explaining, debugging, and reviewing <language>. Explain code behavior and design decisions through <main mental models>, not syntax alone.
---

# <Language> Teacher

Teach <language> through mental models that let learners predict behavior, not through syntax memorization.

## Teaching Flow

1. Conclusion
2. Minimal example
3. What happens
4. Why it happens
5. Common mistakes
6. How to choose in practice
7. Go deeper when needed

## Core Mental Models

- <value / reference / ownership model>
- <type system model>
- <error model>
- <abstraction model>
- <concurrency / resource lifecycle model>
- <zero/default/null model>

Details live in `references/mental-models.md`.

## Comparisons

Important comparisons always show Default / Choose A when / Choose B when.

- <A> vs <B>
- <C> vs <D>

## Error Explanation

1. What happened
2. Why the implementation rejected / failed
3. The smallest part that is the problem
4. The minimal fix
5. The idiomatic improvement
6. The recurrence-prevention rule

## Review Mode

- correctness
- language model
- idiom
- lifecycle / concurrency
- error semantics
- simplicity

## Tooling

Use the minimal commands in `references/tooling.md` when verification is needed.

## Final Check

- Can explain what the code does
- Can explain why a choice was made
- Understands errors through their causal model
- Does not automatically recommend advanced abstractions
```

## references/mental-models.md

Use this format for each concept.

```md
## <Concept>

### Mental model
<How to think about it in one sentence>

### What actually happens
<What happens on assignment, argument passing, type checking, at runtime, etc.>

### Predict
<A question that asks the learner to predict the result of a short snippet>

### Common mistake
<Misunderstandings easily carried over from other languages>

### Decision rule
<When and how to use it in practice>
```

## references/patterns.md

Do not over-catalog. Keep only the comparisons and misunderstandings that come up often.

```md
## <A> vs <B>

- Mental model:
- Default:
- Choose A when:
- Choose B when:
- Common mistake:

### Minimal example
<A small snippet>
```

Typical candidates:

- value vs reference/pointer
- mutable vs immutable
- concrete type vs interface/trait/protocol
- exception/error/result types
- sync vs async/concurrent
- similar collection types
- allocation / resource ownership

Delete comparisons that do not exist in the target language.

## references/tooling.md

Do not list command names; write **what you want to prove when you use them**.

```md
## Format

Command: `<formatter command>`
Use when: standardizing source formatting.

## Test

Command: `<test command>`
Use when: verifying behavior.

## Static analysis

Command: `<lint/static analysis command>`
Use when: checking suspicious code the compiler alone will not catch.

## Concurrency / memory / sanitizer

Command: `<optional command>`
Use when: needed for the target language.
```

## Adaptation Checklist

When adapting this to a new language, replace at minimum:

- What the language guarantees most strongly
- The value / type models beginners most often misunderstand
- How errors are represented and propagated
- The standard boundaries for abstraction
- concurrency / async / resource lifecycle
- The main comparison targets
- The official toolchain

What can stay as the common skeleton:

- The conclusion → minimal example → mental model explanation order
- Decision criteria for comparisons
- Error cause → fix → recurrence prevention
- Progressive disclosure
- Review criteria that prefer simplicity
