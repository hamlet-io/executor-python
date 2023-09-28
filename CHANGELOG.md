# Changelog

## latest (2023-09-28)

#### Fixes

* path to the sh script for set_provider_credentails task
* override of black formatting
#### Refactorings

* legacy bash approach removal
#### Others

* liniting cleanup
* foramtting cleanups
* formatting cleanup

Full set of changes: [`9.25.4...latest`](https://github.com/hamlet-io/executor-python/compare/9.25.4...latest)

## 9.25.4 (2023-06-16)

#### Fixes

* remove stdout from docker login task ([#372](https://github.com/hamlet-io/executor-python/issues/372))
#### Others

* update changelog ([#371](https://github.com/hamlet-io/executor-python/issues/371))

Full set of changes: [`9.25.3...9.25.4`](https://github.com/hamlet-io/executor-python/compare/9.25.3...9.25.4)

## 9.25.3 (2023-01-24)

#### Fixes

* handle import failure for py36 compat ([#370](https://github.com/hamlet-io/executor-python/issues/370))
#### Others

* update changelog ([#369](https://github.com/hamlet-io/executor-python/issues/369))

Full set of changes: [`9.25.2...9.25.3`](https://github.com/hamlet-io/executor-python/compare/9.25.2...9.25.3)

## 9.25.2 (2023-01-23)

#### New Features

* add support for OCI image indexes ([#368](https://github.com/hamlet-io/executor-python/issues/368))
#### Others

* update changelog ([#366](https://github.com/hamlet-io/executor-python/issues/366))

Full set of changes: [`9.25.1...9.25.2`](https://github.com/hamlet-io/executor-python/compare/9.25.1...9.25.2)

## 9.25.1 (2023-01-21)

#### Fixes

* fetch depth for versioning
* install process
* update setuuptools scm version ([#367](https://github.com/hamlet-io/executor-python/issues/367))
* add importlib_resources for backwards compat ([#365](https://github.com/hamlet-io/executor-python/issues/365))
#### Others

* remove debug
* update changelog ([#364](https://github.com/hamlet-io/executor-python/issues/364))

Full set of changes: [`9.25.0...9.25.1`](https://github.com/hamlet-io/executor-python/compare/9.25.0...9.25.1)

## 9.25.0 (2023-01-10)

#### New Features

* add dist option for sentry release ([#358](https://github.com/hamlet-io/executor-python/issues/358))
#### Fixes

* (ci): update the gh action for pypi release ([#363](https://github.com/hamlet-io/executor-python/issues/363))
* zip checking for zip task ([#361](https://github.com/hamlet-io/executor-python/issues/361))
* ecr docker login process ([#359](https://github.com/hamlet-io/executor-python/issues/359))
#### Refactorings

* package management ([#360](https://github.com/hamlet-io/executor-python/issues/360))
#### Others

* update changelog ([#362](https://github.com/hamlet-io/executor-python/issues/362))
* update changelog ([#357](https://github.com/hamlet-io/executor-python/issues/357))

Full set of changes: [`9.24.0...9.25.0`](https://github.com/hamlet-io/executor-python/compare/9.24.0...9.25.0)

## 9.24.0 (2022-10-14)

#### Others

* update changelog ([#356](https://github.com/hamlet-io/executor-python/issues/356))

Full set of changes: [`9.23.1...9.24.0`](https://github.com/hamlet-io/executor-python/compare/9.23.1...9.24.0)

## 9.23.1 (2022-09-16)

#### Fixes

* testing updates
* import
* remove use of transport from httpx client
#### Refactorings

* remove deprecated expo_app_publish param
#### Others

* update changelog ([#353](https://github.com/hamlet-io/executor-python/issues/353))
* fix formatting

Full set of changes: [`9.23.0...9.23.1`](https://github.com/hamlet-io/executor-python/compare/9.23.0...9.23.1)

## 9.23.0 (2022-08-19)

#### New Features

* add support for image management via tasks
#### Refactorings

* test updates for caching and cleanup
* remove context cache used for queries
* changelog share pipeline
* deprecate commands replaced by runbooks and native commands
#### Others

* update changelog ([#348](https://github.com/hamlet-io/executor-python/issues/348))
* update cookiecutter

Full set of changes: [`9.22.0...9.23.0`](https://github.com/hamlet-io/executor-python/compare/9.22.0...9.23.0)

## 9.22.0 (2022-05-27)

#### New Features

* (task): add secrets manager task
* add contract task for SES SMTP password generation
#### Fixes

* resolve root dir to absolute path
#### Refactorings

* remove solution layer from cmdb generation
#### Others

* changelog bump ([#343](https://github.com/hamlet-io/executor-python/issues/343))

Full set of changes: [`9.21.0...9.22.0`](https://github.com/hamlet-io/executor-python/compare/9.21.0...9.22.0)

## 9.21.0 (2022-04-20)

#### New Features

* add image reference listing
#### Fixes

* network configuration params for run task ([#342](https://github.com/hamlet-io/executor-python/issues/342))
#### Others

* changelog bump ([#339](https://github.com/hamlet-io/executor-python/issues/339))

Full set of changes: [`9.20.0...9.21.0`](https://github.com/hamlet-io/executor-python/compare/9.20.0...9.21.0)

## 9.20.0 (2022-04-08)

#### New Features

* aws s3 copy rm tasks
#### Fixes

* formatting
#### Refactorings

* use base commands for build refererences and images
* distutils strtobool
#### Others

* changelog bump ([#334](https://github.com/hamlet-io/executor-python/issues/334))

Full set of changes: [`9.19.1...9.20.0`](https://github.com/hamlet-io/executor-python/compare/9.19.1...9.20.0)

## 9.19.1 (2022-03-31)

#### Fixes

* add hamlet_home_dir back to base options ([#333](https://github.com/hamlet-io/executor-python/issues/333))
#### Others

* changelog bump ([#332](https://github.com/hamlet-io/executor-python/issues/332))

Full set of changes: [`9.19.0...9.19.1`](https://github.com/hamlet-io/executor-python/compare/9.19.0...9.19.1)

## 9.19.0 (2022-03-25)

#### New Features

* add support for bundled engine train releases
#### Others

* changelog bump ([#329](https://github.com/hamlet-io/executor-python/issues/329))
* formatting fixes

Full set of changes: [`9.18.0...9.19.0`](https://github.com/hamlet-io/executor-python/compare/9.18.0...9.19.0)

## 9.18.0 (2022-03-24)

#### New Features

* add bundled shim engine loader ([#328](https://github.com/hamlet-io/executor-python/issues/328))
#### Others

* changelog bump ([#327](https://github.com/hamlet-io/executor-python/issues/327))

Full set of changes: [`9.17.1...9.18.0`](https://github.com/hamlet-io/executor-python/compare/9.17.1...9.18.0)

## 9.17.1 (2022-03-23)

#### Fixes

* engine updates ([#326](https://github.com/hamlet-io/executor-python/issues/326))
* use full engine-core image ([#325](https://github.com/hamlet-io/executor-python/issues/325))
#### Refactorings

* district to district type rename ([#324](https://github.com/hamlet-io/executor-python/issues/324))
#### Others

* changelog bump ([#323](https://github.com/hamlet-io/executor-python/issues/323))

Full set of changes: [`9.17.0...9.17.1`](https://github.com/hamlet-io/executor-python/compare/9.17.0...9.17.1)

## 9.17.0 (2022-03-18)

#### New Features

* add support for providing the district type
* (contract): add aws tasks
#### Fixes

* formatting
* extend read timeout for container image handling
#### Refactorings

* aws ecs run task error handling
* (ci): update pipeline to align with latest cli
#### Others

* changelog bump ([#317](https://github.com/hamlet-io/executor-python/issues/317))
* formatting updates
* formatting
* formatting fixes

Full set of changes: [`9.16.5...9.17.0`](https://github.com/hamlet-io/executor-python/compare/9.16.5...9.17.0)

## 9.16.5 (2022-03-15)

#### Fixes

* engine name provided to install-engine
#### Others

* changelog bump ([#315](https://github.com/hamlet-io/executor-python/issues/315))

Full set of changes: [`9.16.4...9.16.5`](https://github.com/hamlet-io/executor-python/compare/9.16.4...9.16.5)

## 9.16.4 (2022-03-14)

#### Fixes

* deploy parameter name ([#314](https://github.com/hamlet-io/executor-python/issues/314))
#### Others

* changelog bump ([#313](https://github.com/hamlet-io/executor-python/issues/313))

Full set of changes: [`9.16.3...9.16.4`](https://github.com/hamlet-io/executor-python/compare/9.16.3...9.16.4)

## 9.16.3 (2022-03-14)

#### Fixes

* more engine parameters for runners ([#312](https://github.com/hamlet-io/executor-python/issues/312))
#### Others

* changelog bump ([#311](https://github.com/hamlet-io/executor-python/issues/311))

Full set of changes: [`9.16.2...9.16.3`](https://github.com/hamlet-io/executor-python/compare/9.16.2...9.16.3)

## 9.16.2 (2022-03-14)

#### Fixes

* passing engine to automation tasks ([#310](https://github.com/hamlet-io/executor-python/issues/310))
#### Others

* changelog bump ([#309](https://github.com/hamlet-io/executor-python/issues/309))

Full set of changes: [`9.16.1...9.16.2`](https://github.com/hamlet-io/executor-python/compare/9.16.1...9.16.2)

## 9.16.1 (2022-03-14)

#### Fixes

* named params for runner invocation ([#308](https://github.com/hamlet-io/executor-python/issues/308))
#### Others

* changelog bump ([#307](https://github.com/hamlet-io/executor-python/issues/307))

Full set of changes: [`9.16.0...9.16.1`](https://github.com/hamlet-io/executor-python/compare/9.16.0...9.16.1)

## 9.16.0 (2022-03-13)

#### New Features

* bundled engine-core for unicycle ([#305](https://github.com/hamlet-io/executor-python/issues/305))
* add backend exception for missing query results
* add cli decorators for log control
* add support for log formatting control
#### Fixes

* further engine passing updates for commands ([#306](https://github.com/hamlet-io/executor-python/issues/306))
* loading of cli profiles
* setup ordering for setup command
* pass engine context to all backend commands
#### Others

* changelog bump ([#300](https://github.com/hamlet-io/executor-python/issues/300))

Full set of changes: [`9.15.0...9.16.0`](https://github.com/hamlet-io/executor-python/compare/9.15.0...9.16.0)

## 9.15.0 (2022-03-08)

#### New Features

* add support for ecs run task
#### Fixes

* formatting and linting
#### Refactorings

* engine context handling with cli
#### Others

* changelog bump

Full set of changes: [`9.14.3...9.15.0`](https://github.com/hamlet-io/executor-python/compare/9.14.3...9.15.0)

## 9.14.3 (2022-02-22)

#### Fixes

* update jinja to latest release

Full set of changes: [`9.14.2...9.14.3`](https://github.com/hamlet-io/executor-python/compare/9.14.2...9.14.3)

## 9.14.2 (2022-02-01)

#### New Features

* update sentry_release command
#### Fixes

* testing and formatting
* add output dir for binary files
* install process
* add botocore back in
#### Refactorings

* setup cleanup
#### Others

* changelog bump ([#290](https://github.com/hamlet-io/executor-python/issues/290))

Full set of changes: [`9.14.1...9.14.2`](https://github.com/hamlet-io/executor-python/compare/9.14.1...9.14.2)

## 9.14.1 (2022-01-25)

#### Fixes

* initial engine loading missing engine ([#289](https://github.com/hamlet-io/executor-python/issues/289))
#### Others

* changelog bump ([#288](https://github.com/hamlet-io/executor-python/issues/288))

Full set of changes: [`9.14.0...9.14.1`](https://github.com/hamlet-io/executor-python/compare/9.14.0...9.14.1)

## 9.14.0 (2022-01-23)

#### New Features

* (contract): add kms encryption tasks
#### Refactorings

* engine management
#### Others

* changelog bump ([#284](https://github.com/hamlet-io/executor-python/issues/284))

Full set of changes: [`9.13.0...9.14.0`](https://github.com/hamlet-io/executor-python/compare/9.13.0...9.14.0)

## 9.13.0 (2022-01-13)

#### New Features

* add local bash command run task
* add support for ssm sessions
* add simple-term-menu dep
* add selection menu tasks for ec2 and ecs
* add support for proxy tunnels on ssh
* limit tram engine loading
#### Fixes

* tests
* engine override install process
* substitution processing for contract params
* pagination for container tags
#### Others

* changelog bump ([#280](https://github.com/hamlet-io/executor-python/issues/280))

Full set of changes: [`9.12.0...9.13.0`](https://github.com/hamlet-io/executor-python/compare/9.12.0...9.13.0)

## 9.12.0 (2022-01-06)

#### New Features

* (task): add ssh copy file implementation
* add support for runbook execution through cli
* contract execution
* add entrance parameter support
#### Fixes

* formatting
* add fabric as dependency ([#278](https://github.com/hamlet-io/executor-python/issues/278))
* formatting
#### Others

* changelog bump ([#273](https://github.com/hamlet-io/executor-python/issues/273))

Full set of changes: [`9.11.0...9.12.0`](https://github.com/hamlet-io/executor-python/compare/9.11.0...9.12.0)

## 9.11.0 (2021-12-24)

#### New Features

* add support for new lambda_jar image format ([#271](https://github.com/hamlet-io/executor-python/issues/271))
#### Others

* changelog bump ([#272](https://github.com/hamlet-io/executor-python/issues/272))

Full set of changes: [`9.10.2...9.11.0`](https://github.com/hamlet-io/executor-python/compare/9.10.2...9.11.0)

## 9.10.2 (2021-12-24)

#### Fixes

* variable naming for schema
#### Refactorings

* schema generation commands
#### Others

* changelog bump ([#269](https://github.com/hamlet-io/executor-python/issues/269))

Full set of changes: [`9.10.1...9.10.2`](https://github.com/hamlet-io/executor-python/compare/9.10.1...9.10.2)

## 9.10.1 (2021-12-18)

#### Fixes

* quoting for shell params ([#268](https://github.com/hamlet-io/executor-python/issues/268))
#### Others

* changelog bump ([#267](https://github.com/hamlet-io/executor-python/issues/267))

Full set of changes: [`9.10.0...9.10.1`](https://github.com/hamlet-io/executor-python/compare/9.10.0...9.10.1)

## 9.10.0 (2021-12-10)

#### New Features

* layer info updates
#### Others

* changelog bump ([#265](https://github.com/hamlet-io/executor-python/issues/265))

Full set of changes: [`9.9.0...9.10.0`](https://github.com/hamlet-io/executor-python/compare/9.9.0...9.10.0)

## 9.9.0 (2021-11-29)

#### New Features

* (testing): enable full scenario testing
* extend autocomplete support
* update to click 8.x
* add layer and component type info
#### Fixes

* use engine fixture
* tests with command update
#### Refactorings

* osx support for testing
* align account infra to state dir
#### Others

* changelog bump ([#258](https://github.com/hamlet-io/executor-python/issues/258))
* fix formatting

Full set of changes: [`9.8.1...9.9.0`](https://github.com/hamlet-io/executor-python/compare/9.8.1...9.9.0)

## 9.8.1 (2021-11-07)

#### Fixes

* (docs): updates to README
#### Others

* changelog bump ([#256](https://github.com/hamlet-io/executor-python/issues/256))

Full set of changes: [`9.8.0...9.8.1`](https://github.com/hamlet-io/executor-python/compare/9.8.0...9.8.1)

## 9.8.0 (2021-11-07)

#### New Features

* extend expo publish command options
* reference command group
#### Fixes

* (test): use dict check for testing tools
* linting and formatting
* update expo backend commands
#### Refactorings

* remove query command
#### Others

* changelog bump ([#251](https://github.com/hamlet-io/executor-python/issues/251))

Full set of changes: [`9.7.2...9.8.0`](https://github.com/hamlet-io/executor-python/compare/9.7.2...9.8.0)

## 9.7.2 (2021-10-08)

#### Fixes

* package dependency updates
#### Others

* changelog bump ([#249](https://github.com/hamlet-io/executor-python/issues/249))

Full set of changes: [`9.7.1...9.7.2`](https://github.com/hamlet-io/executor-python/compare/9.7.1...9.7.2)

## 9.7.1 (2021-10-05)

#### Fixes

* env preference order for runner
* require install of engine before set
#### Others

* changelog bump ([#246](https://github.com/hamlet-io/executor-python/issues/246))

Full set of changes: [`9.7.0...9.7.1`](https://github.com/hamlet-io/executor-python/compare/9.7.0...9.7.1)

## 9.7.0 (2021-10-04)

#### New Features

* extend testing tooling
#### Fixes

* lock boto3 version
* lock boto deps
* formatting
* run automation properties after construct
#### Refactorings

* remove cfn_nag from CI pipeline
* move the cli cache dir to hamlet home
* make missing home dir fatal
* remove updating checking
#### Docs

* reference install guide for hamlet
#### Others

* changelog bump ([#239](https://github.com/hamlet-io/executor-python/issues/239))

Full set of changes: [`9.6.3...9.7.0`](https://github.com/hamlet-io/executor-python/compare/9.6.3...9.7.0)

## 9.6.3 (2021-09-30)

#### New Features

* extend commit message support
#### Fixes

* (runner): boolean string conversion
#### Refactorings

* allow for overriding defer_push
#### Others

* changelog bump ([#237](https://github.com/hamlet-io/executor-python/issues/237))
* changelog bump ([#234](https://github.com/hamlet-io/executor-python/issues/234))

Full set of changes: [`9.6.2...9.6.3`](https://github.com/hamlet-io/executor-python/compare/9.6.2...9.6.3)

## 9.6.2 (2021-09-26)

#### Fixes

* determine tree before context
* handle container registry update failures
#### Others

* linting updates
* liniting fixes

Full set of changes: [`9.6.1...9.6.2`](https://github.com/hamlet-io/executor-python/compare/9.6.1...9.6.2)

## 9.6.1 (2021-09-15)

#### Fixes

* httpx package dep changes
#### Others

* changelog bump ([#232](https://github.com/hamlet-io/executor-python/issues/232))
* changelog bump ([#219](https://github.com/hamlet-io/executor-python/issues/219))

Full set of changes: [`9.6.0...9.6.1`](https://github.com/hamlet-io/executor-python/compare/9.6.0...9.6.1)

## 9.6.0 (2021-09-06)

#### New Features

* add cmdb save command
* add occurrences query
#### Fixes

* handle user facing errors
* tests and handle result types
* provide details to set context for automation
* use content digest as container digests
#### Refactorings

* only get properties if required
#### Others

* linting updates
* linting fixes
* linting fixes
* update engine install documentation ([#222](https://github.com/hamlet-io/executor-python/issues/222))

Full set of changes: [`9.5.0...9.6.0`](https://github.com/hamlet-io/executor-python/compare/9.5.0...9.6.0)

## 9.5.0 (2021-08-08)

#### New Features

* user defined engines
* add local directory engine source
* add district based deployment filters
#### Fixes

* clean engine argument handling
* rename config file option to reflect reality
#### Refactorings

* config directory handling
* move loaders to their own modules
#### Docs

* add basic class docs for the config files
#### Others

* changelog bump ([#216](https://github.com/hamlet-io/executor-python/issues/216))
* linting fixes

Full set of changes: [`9.4.0...9.5.0`](https://github.com/hamlet-io/executor-python/compare/9.4.0...9.5.0)

## 9.4.0 (2021-07-16)

#### New Features

* engine install control and get engine
#### Fixes

* wrong function call for digest ([#215](https://github.com/hamlet-io/executor-python/issues/215))
* add description
* (ci): update repository url
#### Others

* changelog bump ([#212](https://github.com/hamlet-io/executor-python/issues/212))

Full set of changes: [`9.3.0...9.4.0`](https://github.com/hamlet-io/executor-python/compare/9.3.0...9.4.0)

## 9.3.0 (2021-07-10)

#### New Features

* rename hamlet package
* make the train engine the default
* add auto generated reference docs
* show envvars for root command options
#### Fixes

* update docs nd make
#### Refactorings

* general docs updates and tidy up
#### Others

* changelog bump ([#204](https://github.com/hamlet-io/executor-python/issues/204))
* changelog bump ([#201](https://github.com/hamlet-io/executor-python/issues/201))

Full set of changes: [`9.2.0...9.3.0`](https://github.com/hamlet-io/executor-python/compare/9.2.0...9.3.0)

## 9.2.0 (2021-07-09)

#### New Features

* add tests for release commands
* release commands
* add manage images command
* automation task runners
* wrap the basic automation commands
* allow the runner to be used for automation
#### Fixes

* handle engine set via env var
* allow for shared image formats
* add environment to align with promote
* default engine notification during install
#### Refactorings

* remove env from image transfer
* backend automation tasks
* realign backend tasks to handle testing
#### Others

* formatting fixes
* formatting updates
* formatting and linting

Full set of changes: [`9.1.1...9.2.0`](https://github.com/hamlet-io/executor-python/compare/9.1.1...9.2.0)

## 9.1.1 (2021-07-06)

#### New Features

* add support for black code formatting
#### Fixes

* (deploy): include options when running deploys ([#200](https://github.com/hamlet-io/executor-python/issues/200))
#### Refactorings

* component commands ([#199](https://github.com/hamlet-io/executor-python/issues/199))
* linting fixes
* apply formatting
#### Others

* changelog bump ([#198](https://github.com/hamlet-io/executor-python/issues/198))

Full set of changes: [`9.1.0...9.1.1`](https://github.com/hamlet-io/executor-python/compare/9.1.0...9.1.1)

## 9.1.0 (2021-07-03)

#### New Features

* default to options for engine install
#### Refactorings

* set engine use local first
* updating handling for engines
#### Others

* changelog bump ([#193](https://github.com/hamlet-io/executor-python/issues/193))
* linting fixes

Full set of changes: [`9.0.2...9.1.0`](https://github.com/hamlet-io/executor-python/compare/9.0.2...9.1.0)

## 9.0.2 (2021-07-01)

#### Fixes

* release pattern for release condition

Full set of changes: [`9.0.1...9.0.2`](https://github.com/hamlet-io/executor-python/compare/9.0.1...9.0.2)

## 9.0.1 (2021-07-01)

#### Fixes

* (ci): move release job into single workflow ([#194](https://github.com/hamlet-io/executor-python/issues/194))
* typo
* changelog details
#### Refactorings

* (engine): align unicycle docker tags
#### Others

* changelog bump ([#190](https://github.com/hamlet-io/executor-python/issues/190))

Full set of changes: [`9.0.0...9.0.1`](https://github.com/hamlet-io/executor-python/compare/9.0.0...9.0.1)

## 9.0.0 (2021-06-30)

#### New Features

* removes the query command group
* deprecate the query command group
* add dynamic engine loaders tram and train
* show hidden engines in cli
* adds support for getting container tags
* (engine): add the wrapper into the tram
* auto update the global engine
* add wrapper to unicycle loader
* handle out of date global engine
* detailed engine information ([#167](https://github.com/hamlet-io/executor-python/issues/167))
* include cli version in command
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

* testing
* build detail path splitting
* tests
* use context manager for generate
* handle invalid versions for engine loading
* handle  instllation process and global env
* handle broken engines
* remove local version from scm
* options passed to backend query for diagrams
* version bump
* set title to package name ([#163](https://github.com/hamlet-io/executor-python/issues/163))
* changelog command
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

* align tests with backend move for deploy
* align with backend deploy move
* move deploy functions to backend
* remove networkx fixed dependecy
* engine update handling
* project layout ([#173](https://github.com/hamlet-io/executor-python/issues/173))
* move to scm based versioning ([#172](https://github.com/hamlet-io/executor-python/issues/172))
* (ci): release trigger process ([#164](https://github.com/hamlet-io/executor-python/issues/164))
* remove jenkinsfile docker trigger
* move engine name to argument
* update commands to align with backend
* updates and documentation
#### Others

* changelog bump ([#165](https://github.com/hamlet-io/executor-python/issues/165))
* liniting fixes
* version bump ([#170](https://github.com/hamlet-io/executor-python/issues/170))
* version bump ([#169](https://github.com/hamlet-io/executor-python/issues/169))
* version bump ([#168](https://github.com/hamlet-io/executor-python/issues/168))
* release bump [skip actions] ([#157](https://github.com/hamlet-io/executor-python/issues/157))
* release bump [skip actions] ([#156](https://github.com/hamlet-io/executor-python/issues/156))
* release bump [skip actions] ([#154](https://github.com/hamlet-io/executor-python/issues/154))
* release bump [skip actions] ([#153](https://github.com/hamlet-io/executor-python/issues/153))
* release bump [skip actions]
* release bump [skip actions] ([#148](https://github.com/hamlet-io/executor-python/issues/148))
* release bump [skip actions] ([#144](https://github.com/hamlet-io/executor-python/issues/144))
* release bump [skip actions] ([#141](https://github.com/hamlet-io/executor-python/issues/141))
* linting updates
* release bump [skip actions] ([#140](https://github.com/hamlet-io/executor-python/issues/140))
* update cli package version ([#137](https://github.com/hamlet-io/executor-python/issues/137))

Full set of changes: [`8.1.2...9.0.0`](https://github.com/hamlet-io/executor-python/compare/8.1.2...9.0.0)

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
