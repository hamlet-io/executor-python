# Changelog

## Unreleased (2021-06-21)

#### New Features

* add support for engine updates
* allow dryn runs on create  actions
* update docs to outline install process
* add tests for commands and backend
* integrate engine management with cli
* add engine command to cli
* add docker-registry packages
* engine management commands
* add engine management backend
* container registry helper functions
#### Fixes

* align env with arg
* handle permissions on home dir
* more descriptions on packages and add dos2unix
* wording fixes in docs
* update wording on container registry
* documentation and env setup
* handling of default and global engines
* support global args when not required
* logging during cli execptions
#### Refactorings

* remove jenkinsfile docker trigger
* move engine name to argument
* update commands to align with backend
* updates and documentation
#### Others

* release bump [skip actions] ([#154](https://github.com/hamlet-io/executor-python/issues/154))
* release bump [skip actions] ([#153](https://github.com/hamlet-io/executor-python/issues/153))
* release bump [skip actions]
* release bump [skip actions] ([#148](https://github.com/hamlet-io/executor-python/issues/148))
* release bump [skip actions] ([#144](https://github.com/hamlet-io/executor-python/issues/144))
* release bump [skip actions] ([#141](https://github.com/hamlet-io/executor-python/issues/141))
* linting updates
* release bump [skip actions] ([#140](https://github.com/hamlet-io/executor-python/issues/140))
* update cli package version ([#137](https://github.com/hamlet-io/executor-python/issues/137))

Full set of changes: [`8.1.2...fde4c5a`](https://github.com/hamlet-io/executor-python/compare/8.1.2...fde4c5a)

## 8.1.2 (2021-05-13)

#### Fixes

* include cookie cutter templates in packag ([#135](https://github.com/hamlet-io/executor-python/issues/135))
* revert testing for cmdb generate
* include setup packages in test
* importlib package name
* include importlib_resources in setup
* bump release to next dev release ([#131](https://github.com/hamlet-io/executor-python/issues/131))
#### Refactorings

* clean up dockerfile
* align commands with simple sytnax
* update testing for new command layout
* migrates cookie cutter templates to cli
#### Others

* bump changelog
* release bump [skip actions] ([#136](https://github.com/hamlet-io/executor-python/issues/136))
* release bump [skip actions] ([#133](https://github.com/hamlet-io/executor-python/issues/133))
* liniting fixes
* release bump [skip actions] ([#132](https://github.com/hamlet-io/executor-python/issues/132))
* (deps): bump lodash from 4.17.20 to 4.17.21 ([#130](https://github.com/hamlet-io/executor-python/issues/130))
* (deps): bump hosted-git-info from 2.8.8 to 2.8.9 ([#128](https://github.com/hamlet-io/executor-python/issues/128))
* (deps): bump handlebars from 4.7.6 to 4.7.7 ([#127](https://github.com/hamlet-io/executor-python/issues/127))
* release bump [skip actions] ([#126](https://github.com/hamlet-io/executor-python/issues/126))

Full set of changes: [`8.1.0, 8.1.1...8.1.2`](https://github.com/hamlet-io/executor-python/compare/8.1.0, 8.1.1...8.1.2)

## 8.1.0, 8.1.1 (2021-05-03)

#### New Features

* add dryrun tasks to run deployment
* use raw name and id for occurrences
* add relesae support for cli ([#111](https://github.com/hamlet-io/executor-python/issues/111))
* add test deployments command ([#110](https://github.com/hamlet-io/executor-python/issues/110))
* update message
* update message
* update message
* add packaging  support
* Component command group ([#99](https://github.com/hamlet-io/executor-python/issues/99))
* Deployment state support ([#94](https://github.com/hamlet-io/executor-python/issues/94))
* add root_dir as common option ([#88](https://github.com/hamlet-io/executor-python/issues/88))
* add different development processes ([#90](https://github.com/hamlet-io/executor-python/issues/90))
* generate command quality of life ([#86](https://github.com/hamlet-io/executor-python/issues/86))
* setup command ([#87](https://github.com/hamlet-io/executor-python/issues/87))
* multiple diagram generation
* district config via profiles ([#79](https://github.com/hamlet-io/executor-python/issues/79))
* diagram generation from cli ([#75](https://github.com/hamlet-io/executor-python/issues/75))
* hamlet schema command set ([#73](https://github.com/hamlet-io/executor-python/issues/73))
* (generate): support provider types in account ([#72](https://github.com/hamlet-io/executor-python/issues/72))
* azure deploy and better exception handling
* clean hanlding of script failures
* changelog generation ([#69](https://github.com/hamlet-io/executor-python/issues/69))
* add diagrams depdencies for visual ([#67](https://github.com/hamlet-io/executor-python/issues/67))
* filter list-deployments in line with commands
* (deploy): always appened end of line pattern
* add create deployments and rework run deployments
* add deploy command
* add support for diagram plugin generation and execution
* add support for entrances ([#55](https://github.com/hamlet-io/executor-python/issues/55))
* support additonal pytest arguments on run ([#52](https://github.com/hamlet-io/executor-python/issues/52))
* add schema level test
* (schema): add template level of schema for schema generation
#### Fixes

* set base branch for release pr
* syntax error in github action
* tag name config for release
* tag release handling
* run release versions based on created release ([#125](https://github.com/hamlet-io/executor-python/issues/125))
* test updates for raw name
* log engine fatal messages on failure
* align releases for pypi
* use pull release for version bump ([#113](https://github.com/hamlet-io/executor-python/issues/113))
* packaging support for pypi ([#112](https://github.com/hamlet-io/executor-python/issues/112))
* package config
* add readme for package ([#109](https://github.com/hamlet-io/executor-python/issues/109))
* repo url in changelogs
* remove debug statement
* skip refresh for orphaned deployments
* handle large outputs in runner calls ([#95](https://github.com/hamlet-io/executor-python/issues/95))
* output_dir paramter not required ([#92](https://github.com/hamlet-io/executor-python/issues/92))
* recreate child readme as symlink
* add output_dir to manage deployment
* make provider input supoprt multiple ([#65](https://github.com/hamlet-io/executor-python/issues/65))
* missing level deployment group renames ([#64](https://github.com/hamlet-io/executor-python/issues/64))
* handle ints in table outputs
* testing root dir location
* postinstall docker
* test and linting
* allow for int outputs in tables
* reference command reference to cot
#### Refactorings

* clean up cli install
* use setup.py for production requirements
* find available bash install when calling
* update basic install docs
* backend exception handling in cli ([#96](https://github.com/hamlet-io/executor-python/issues/96))
* options context and generation parameters ([#89](https://github.com/hamlet-io/executor-python/issues/89))
* move github templates to org
* use rawId in query outputs ([#77](https://github.com/hamlet-io/executor-python/issues/77))
* handle backend exceptions in cli
* use fullmatch re pattern
* support running tests from any clone of repo
* deployment-group migration from level
* rename from cot to hamlet
* update to hamlet structure and image
#### Docs

* README overhaul
#### Others

* 8.1.0 release notes
* release bump [skip actions] ([#123](https://github.com/hamlet-io/executor-python/issues/123))
* release bump [skip actions] ([#120](https://github.com/hamlet-io/executor-python/issues/120))
* release bump [skip actions] ([#116](https://github.com/hamlet-io/executor-python/issues/116))
* release bump [skip actions] ([#114](https://github.com/hamlet-io/executor-python/issues/114))
* release notes
* (deps): bump jinja2 in /hamlet-cli/requirements ([#106](https://github.com/hamlet-io/executor-python/issues/106))
* remove hamlet-cli individual readme
* remove outdated ref to codeontap
* changelog
* changelog
* update package depdencies
