# Static Quality

TypeScript、Lint、Format、Dead Code Detectionを扱う。

## TypeScript

まず現在のcompiler configurationを確認する。

評価対象:

- strict type checking
- unused declarations
- unsafe fallthrough
- module semantics
- side-effect imports
- framework-generated types

厳しい設定ほど良いとは限らない。導入時にはapplication code、tests、generated code、build tools、framework、library typingsへの影響を見る。

大量の既存errorを発生させる設定変更は、独立したmigrationとして扱う。

## Lint

Lintの目的はrule数を増やすことではない。

優先するもの:

- correctness
- common bug detection
- unsafe patterns
- project conventions
- framework-specific mistakes

単なるstylistic preferenceはformatterに任せられないか検討する。

既存linterを別のlinterへ変更する場合は明確な理由を必要とする。候補となる理由は、feedbackの大幅な高速化、configuration complexityの削減、duplicated toolingの削減、migration costの小ささなど。

## Format

formattingは可能な限り機械的に処理する。

Agentや開発者へformatting styleを暗記させる設計を避ける。formatterが存在する場合、lintと責務が重複していないか確認する。

## Dead code

Agentによる高速な変更では不要コードが蓄積しやすいため、dead code detectionを検討する。

対象:

- unused files
- unused exports
- unused dependencies
- unused devDependencies

ただしframework entry points、generated files、configuration files、migrations、test utilities、registry-based loading、dynamic importsはfalse positiveが発生しやすい。

全体ignoreより、狭いexceptionを優先する。

## Static analysis responsibilities

可能なら責務を分離する。

- Compiler: type correctness
- Linter: bug patterns、unsafe code、conventions
- Formatter: formatting
- Dead-code analyzer: unreachable or unused project artifacts

同じ問題を複数toolで重複検査しない。
