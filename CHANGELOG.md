# [0.0.0](https://github.com/hamlet-io/executor-python/compare/8.1.2...0.0.0) (2021-05-13)



## [8.1.2](https://github.com/hamlet-io/executor-python/compare/8.1.1...8.1.2) (2021-05-13)


### Bug Fixes

* bump release to next dev release ([#131](https://github.com/hamlet-io/executor-python/issues/131)) ([55666c7](https://github.com/hamlet-io/executor-python/commit/55666c75fa383a85bd6112a4f616ca5145e6d157))
* importlib package name ([a3e6a57](https://github.com/hamlet-io/executor-python/commit/a3e6a571be6591ee05622cf4570178606bcc1c00))
* include cookie cutter templates in packag ([#135](https://github.com/hamlet-io/executor-python/issues/135)) ([b51637c](https://github.com/hamlet-io/executor-python/commit/b51637c3bd8169f79c8c3a9deccc244b53885d37))
* include importlib_resources in setup ([a33101e](https://github.com/hamlet-io/executor-python/commit/a33101e76b59ef29da18b5d1a4b89e01d44d812f))
* include setup packages in test ([71f087f](https://github.com/hamlet-io/executor-python/commit/71f087f2a8ae561de8ec9b15abf7442adb3249fa))
* revert testing for cmdb generate ([b54402c](https://github.com/hamlet-io/executor-python/commit/b54402c80fe037fc530ca9569f8c5579ecb4b59b))



## [8.1.1](https://github.com/hamlet-io/executor-python/compare/8.1.0...8.1.1) (2021-05-03)


### Bug Fixes

* add readme for package ([#109](https://github.com/hamlet-io/executor-python/issues/109)) ([3a225d3](https://github.com/hamlet-io/executor-python/commit/3a225d307918ad03fda08a81476a31c6a6b8c158))
* align releases for pypi ([0befba9](https://github.com/hamlet-io/executor-python/commit/0befba9f3d5e39f8f7239d19057a7f2f65cf6e15))
* log engine fatal messages on failure ([fd6defe](https://github.com/hamlet-io/executor-python/commit/fd6defeb6d389fe914732a11ac4f35370f71ad8b))
* package config ([01ca58c](https://github.com/hamlet-io/executor-python/commit/01ca58c49949441da7ddfb82a996901dbcdbe8a6))
* packaging support for pypi ([#112](https://github.com/hamlet-io/executor-python/issues/112)) ([9f254cf](https://github.com/hamlet-io/executor-python/commit/9f254cfa9e75c88f94ecb933eed3b282af161dfd))
* repo url in changelogs ([62b556e](https://github.com/hamlet-io/executor-python/commit/62b556e131d23cbca75d672fd66b9e45b2881e23))
* run release versions based on created release ([#125](https://github.com/hamlet-io/executor-python/issues/125)) ([2fa5998](https://github.com/hamlet-io/executor-python/commit/2fa5998d0f257e8050a66dda3e0ed58c3536ecf5))
* set base branch for release pr ([7fbf5d2](https://github.com/hamlet-io/executor-python/commit/7fbf5d2d26a1ac776dc0741077be52130a2b9525))
* syntax error in github action ([f833fa5](https://github.com/hamlet-io/executor-python/commit/f833fa541d10db999957b3497c280922c3d78757))
* tag name config for release ([eb82dfb](https://github.com/hamlet-io/executor-python/commit/eb82dfb8848cc4f13b353b897d6c63fed85ab3bf))
* tag release handling ([f1d19c3](https://github.com/hamlet-io/executor-python/commit/f1d19c3ee75c8e3b8f3be6295f703500b136a2df))
* test updates for raw name ([f468f08](https://github.com/hamlet-io/executor-python/commit/f468f084ad387881d28e1c21945a1302246a3b3c))
* use pull release for version bump ([#113](https://github.com/hamlet-io/executor-python/issues/113)) ([5d962e1](https://github.com/hamlet-io/executor-python/commit/5d962e17f37cdea4b90c52a691defe03db3acf6c))


### Features

* add dryrun tasks to run deployment ([d714390](https://github.com/hamlet-io/executor-python/commit/d7143906a941b3bf90ad928e09f22f9ac1ad7b8f))
* add packaging  support ([0c65f40](https://github.com/hamlet-io/executor-python/commit/0c65f4079ca732c8cb07da6cdcf0ab0d62a02d74))
* add relesae support for cli ([#111](https://github.com/hamlet-io/executor-python/issues/111)) ([cce8e47](https://github.com/hamlet-io/executor-python/commit/cce8e4726cf651f3f524e94e66af35d718312e06))
* add test deployments command ([#110](https://github.com/hamlet-io/executor-python/issues/110)) ([fe1058b](https://github.com/hamlet-io/executor-python/commit/fe1058be69610a2f88ccd8a840eba8d408be24c5))
* update message ([d6223db](https://github.com/hamlet-io/executor-python/commit/d6223dbc42729131e8e57b5ff7cb275ebdb4b533))
* update message ([bbd2a7a](https://github.com/hamlet-io/executor-python/commit/bbd2a7ac994dd3235fdfe8cbe6db70371fee7e3a))
* update message ([ddd78e9](https://github.com/hamlet-io/executor-python/commit/ddd78e9d3e8227d335dd9a716e5bcfb786d1261b))
* use raw name and id for occurrences ([7765f5c](https://github.com/hamlet-io/executor-python/commit/7765f5c2de371f9151e696b49d3a2dac3361cd72))



## [8.0.1](https://github.com/hamlet-io/executor-python/compare/v8.0.0...v8.0.1) (2021-03-20)


### Bug Fixes

* add output_dir to manage deployment ([5b107f2](https://github.com/hamlet-io/executor-python/commit/5b107f244cfe095971c2fc30bbe2d8b9009acace))
* handle large outputs in runner calls ([#95](https://github.com/hamlet-io/executor-python/issues/95)) ([e4dd943](https://github.com/hamlet-io/executor-python/commit/e4dd943796a0ae0d169c2bac7802770e101d381c))
* output_dir paramter not required ([#92](https://github.com/hamlet-io/executor-python/issues/92)) ([2d3f5ac](https://github.com/hamlet-io/executor-python/commit/2d3f5acce2e0be9a5e17b21a9bafb827ff3d67bd))
* recreate child readme as symlink ([7a19c70](https://github.com/hamlet-io/executor-python/commit/7a19c70acab6d98f70022982143027188e70c882))
* remove debug statement ([73263e6](https://github.com/hamlet-io/executor-python/commit/73263e640174b662e1f1bf0f5e8009affe01633d))
* skip refresh for orphaned deployments ([5141743](https://github.com/hamlet-io/executor-python/commit/5141743b277019252a92d83bb38c8637d2a2bbbb))


### Features

* add different development processes ([#90](https://github.com/hamlet-io/executor-python/issues/90)) ([34f51ec](https://github.com/hamlet-io/executor-python/commit/34f51ec253956eb3c28344a7aa5ef93355634353))
* add root_dir as common option ([#88](https://github.com/hamlet-io/executor-python/issues/88)) ([2eefd21](https://github.com/hamlet-io/executor-python/commit/2eefd21a02929ed96ec194e27a2fd032171c044f))
* azure deploy and better exception handling ([4908dda](https://github.com/hamlet-io/executor-python/commit/4908ddaea7dddddd26a52b83d5f1292ba0976c2d))
* clean hanlding of script failures ([47b8ba0](https://github.com/hamlet-io/executor-python/commit/47b8ba0601f793748546c13b94440702cd628f98))
* Component command group ([#99](https://github.com/hamlet-io/executor-python/issues/99)) ([7503146](https://github.com/hamlet-io/executor-python/commit/7503146f7a94e1c81f0cc00b06beea399709a7ad))
* Deployment state support ([#94](https://github.com/hamlet-io/executor-python/issues/94)) ([742b1db](https://github.com/hamlet-io/executor-python/commit/742b1dbee48a670f18b0d05aa1ed20e1066b47d8))
* diagram generation from cli ([#75](https://github.com/hamlet-io/executor-python/issues/75)) ([4bebf39](https://github.com/hamlet-io/executor-python/commit/4bebf39c85a28b09db9a65b8ee3111c01d141233))
* district config via profiles ([#79](https://github.com/hamlet-io/executor-python/issues/79)) ([0b0434e](https://github.com/hamlet-io/executor-python/commit/0b0434eb8bdaab8b889488121ccab008198d07f0))
* generate command quality of life ([#86](https://github.com/hamlet-io/executor-python/issues/86)) ([222a17d](https://github.com/hamlet-io/executor-python/commit/222a17d2c72e3f42c0bf127af52c80dbf64972ea))
* hamlet schema command set ([#73](https://github.com/hamlet-io/executor-python/issues/73)) ([e31d570](https://github.com/hamlet-io/executor-python/commit/e31d5703cdde2d0bed57fd57600ed8aa6256421e))
* multiple diagram generation ([316e695](https://github.com/hamlet-io/executor-python/commit/316e69500c1f8f326a35146104ec6446b10c0e1c))
* setup command ([#87](https://github.com/hamlet-io/executor-python/issues/87)) ([6a1d0c8](https://github.com/hamlet-io/executor-python/commit/6a1d0c85a6fea7560236e38c6e5e524cec03644a))
* **generate:** support provider types in account ([#72](https://github.com/hamlet-io/executor-python/issues/72)) ([97b15fd](https://github.com/hamlet-io/executor-python/commit/97b15fd682f3cb9db50d92d125481d564c682903))



# [8.0.0](https://github.com/hamlet-io/executor-python/compare/v7.0.0...v8.0.0) (2021-01-11)


### Bug Fixes

* allow for int outputs in tables ([cc470ce](https://github.com/hamlet-io/executor-python/commit/cc470ce670b002b317aebec408a9dee5a6a26ba2))
* handle ints in table outputs ([72416ee](https://github.com/hamlet-io/executor-python/commit/72416eee0a73d8d191c209c68d27835418eddd22))
* make provider input supoprt multiple ([#65](https://github.com/hamlet-io/executor-python/issues/65)) ([6f3eab3](https://github.com/hamlet-io/executor-python/commit/6f3eab3d3033ecc5e5144d7b5708499eb0693148))
* missing level deployment group renames ([#64](https://github.com/hamlet-io/executor-python/issues/64)) ([dc808e4](https://github.com/hamlet-io/executor-python/commit/dc808e414cf66f27baddb030aec0dfd12509053c))
* postinstall docker ([e9976e1](https://github.com/hamlet-io/executor-python/commit/e9976e18b14a03356a04c3ca811b7bf6e1a13e03))
* reference command reference to cot ([0702c4b](https://github.com/hamlet-io/executor-python/commit/0702c4bea17775810ce9b60ae7c7e8ce957fea42))
* remove testcase and scenario inputs to align with bash ([ff339ef](https://github.com/hamlet-io/executor-python/commit/ff339efc824bbcec80b27b343d8d1bc770830a73))
* test and linting ([b0d7e86](https://github.com/hamlet-io/executor-python/commit/b0d7e86d860330106c0c877163a885914a68e449))
* testing root dir location ([170ea45](https://github.com/hamlet-io/executor-python/commit/170ea4556d5d506a7d071a3edfb93f875cb726c9))


### Features

* add create deployments and rework run deployments ([6279ee9](https://github.com/hamlet-io/executor-python/commit/6279ee992a538a98499297a710d36f88c12778f9))
* add deploy command ([bb264cd](https://github.com/hamlet-io/executor-python/commit/bb264cd72e2060d67448b2281051accd33f127b9))
* add diagrams depdencies for visual ([#67](https://github.com/hamlet-io/executor-python/issues/67)) ([cb6f945](https://github.com/hamlet-io/executor-python/commit/cb6f945add04bc8c5887fae12f8401422a08c2c0))
* add schema level test ([c77521c](https://github.com/hamlet-io/executor-python/commit/c77521c58dfbdb3d9d277f158578dd4a56d8125c))
* add support for diagram plugin generation and execution ([59d24d3](https://github.com/hamlet-io/executor-python/commit/59d24d370cd0e2312e753d47178d3cb015a0a2cb))
* add support for entrances ([#55](https://github.com/hamlet-io/executor-python/issues/55)) ([3e31422](https://github.com/hamlet-io/executor-python/commit/3e3142276ff14e5e99f297fee672f6af4bb62b59))
* changelog generation ([#69](https://github.com/hamlet-io/executor-python/issues/69)) ([ff7585f](https://github.com/hamlet-io/executor-python/commit/ff7585fc573f8cd01b62ab747c2fdcdd6ead0f4d))
* filter list-deployments in line with commands ([90d8b82](https://github.com/hamlet-io/executor-python/commit/90d8b82c96bab3176fb20e9edaec94d0ba544b2a))
* **deploy:** always appened end of line pattern ([646b4fe](https://github.com/hamlet-io/executor-python/commit/646b4fe59fe18ede3ccd648df9e2268a96401429))
* support additonal pytest arguments on run ([#52](https://github.com/hamlet-io/executor-python/issues/52)) ([983508a](https://github.com/hamlet-io/executor-python/commit/983508ab3ed7b1f55914d16a069f588b13a36f08))
* **schema:** add template level of schema for schema generation ([ae89c0d](https://github.com/hamlet-io/executor-python/commit/ae89c0d12e30077db2ae9b2ca4be4236e81a7138))



# 7.0.0 (2020-03-20)



