# [0.0.0](https://github.com/hamlet-io/engine-plugin-aws/compare/v8.0.1...v0.0.0) (2021-03-30)



## [8.0.1](https://github.com/hamlet-io/engine-plugin-aws/compare/v8.0.0...v8.0.1) (2021-03-20)


### Bug Fixes

* add output_dir to manage deployment ([5b107f2](https://github.com/hamlet-io/engine-plugin-aws/commit/5b107f244cfe095971c2fc30bbe2d8b9009acace))
* handle large outputs in runner calls ([#95](https://github.com/hamlet-io/engine-plugin-aws/issues/95)) ([e4dd943](https://github.com/hamlet-io/engine-plugin-aws/commit/e4dd943796a0ae0d169c2bac7802770e101d381c))
* output_dir paramter not required ([#92](https://github.com/hamlet-io/engine-plugin-aws/issues/92)) ([2d3f5ac](https://github.com/hamlet-io/engine-plugin-aws/commit/2d3f5acce2e0be9a5e17b21a9bafb827ff3d67bd))
* recreate child readme as symlink ([7a19c70](https://github.com/hamlet-io/engine-plugin-aws/commit/7a19c70acab6d98f70022982143027188e70c882))
* remove debug statement ([73263e6](https://github.com/hamlet-io/engine-plugin-aws/commit/73263e640174b662e1f1bf0f5e8009affe01633d))
* skip refresh for orphaned deployments ([5141743](https://github.com/hamlet-io/engine-plugin-aws/commit/5141743b277019252a92d83bb38c8637d2a2bbbb))


### Features

* add different development processes ([#90](https://github.com/hamlet-io/engine-plugin-aws/issues/90)) ([34f51ec](https://github.com/hamlet-io/engine-plugin-aws/commit/34f51ec253956eb3c28344a7aa5ef93355634353))
* add root_dir as common option ([#88](https://github.com/hamlet-io/engine-plugin-aws/issues/88)) ([2eefd21](https://github.com/hamlet-io/engine-plugin-aws/commit/2eefd21a02929ed96ec194e27a2fd032171c044f))
* azure deploy and better exception handling ([4908dda](https://github.com/hamlet-io/engine-plugin-aws/commit/4908ddaea7dddddd26a52b83d5f1292ba0976c2d))
* clean hanlding of script failures ([47b8ba0](https://github.com/hamlet-io/engine-plugin-aws/commit/47b8ba0601f793748546c13b94440702cd628f98))
* Component command group ([#99](https://github.com/hamlet-io/engine-plugin-aws/issues/99)) ([7503146](https://github.com/hamlet-io/engine-plugin-aws/commit/7503146f7a94e1c81f0cc00b06beea399709a7ad))
* **generate:** support provider types in account ([#72](https://github.com/hamlet-io/engine-plugin-aws/issues/72)) ([97b15fd](https://github.com/hamlet-io/engine-plugin-aws/commit/97b15fd682f3cb9db50d92d125481d564c682903))
* Deployment state support ([#94](https://github.com/hamlet-io/engine-plugin-aws/issues/94)) ([742b1db](https://github.com/hamlet-io/engine-plugin-aws/commit/742b1dbee48a670f18b0d05aa1ed20e1066b47d8))
* diagram generation from cli ([#75](https://github.com/hamlet-io/engine-plugin-aws/issues/75)) ([4bebf39](https://github.com/hamlet-io/engine-plugin-aws/commit/4bebf39c85a28b09db9a65b8ee3111c01d141233))
* district config via profiles ([#79](https://github.com/hamlet-io/engine-plugin-aws/issues/79)) ([0b0434e](https://github.com/hamlet-io/engine-plugin-aws/commit/0b0434eb8bdaab8b889488121ccab008198d07f0))
* generate command quality of life ([#86](https://github.com/hamlet-io/engine-plugin-aws/issues/86)) ([222a17d](https://github.com/hamlet-io/engine-plugin-aws/commit/222a17d2c72e3f42c0bf127af52c80dbf64972ea))
* hamlet schema command set ([#73](https://github.com/hamlet-io/engine-plugin-aws/issues/73)) ([e31d570](https://github.com/hamlet-io/engine-plugin-aws/commit/e31d5703cdde2d0bed57fd57600ed8aa6256421e))
* multiple diagram generation ([316e695](https://github.com/hamlet-io/engine-plugin-aws/commit/316e69500c1f8f326a35146104ec6446b10c0e1c))
* setup command ([#87](https://github.com/hamlet-io/engine-plugin-aws/issues/87)) ([6a1d0c8](https://github.com/hamlet-io/engine-plugin-aws/commit/6a1d0c85a6fea7560236e38c6e5e524cec03644a))



# [8.0.0](https://github.com/hamlet-io/engine-plugin-aws/compare/v7.0.0...v8.0.0) (2021-01-11)


### Bug Fixes

* allow for int outputs in tables ([cc470ce](https://github.com/hamlet-io/engine-plugin-aws/commit/cc470ce670b002b317aebec408a9dee5a6a26ba2))
* handle ints in table outputs ([72416ee](https://github.com/hamlet-io/engine-plugin-aws/commit/72416eee0a73d8d191c209c68d27835418eddd22))
* make provider input supoprt multiple ([#65](https://github.com/hamlet-io/engine-plugin-aws/issues/65)) ([6f3eab3](https://github.com/hamlet-io/engine-plugin-aws/commit/6f3eab3d3033ecc5e5144d7b5708499eb0693148))
* missing level deployment group renames ([#64](https://github.com/hamlet-io/engine-plugin-aws/issues/64)) ([dc808e4](https://github.com/hamlet-io/engine-plugin-aws/commit/dc808e414cf66f27baddb030aec0dfd12509053c))
* postinstall docker ([e9976e1](https://github.com/hamlet-io/engine-plugin-aws/commit/e9976e18b14a03356a04c3ca811b7bf6e1a13e03))
* reference command reference to cot ([0702c4b](https://github.com/hamlet-io/engine-plugin-aws/commit/0702c4bea17775810ce9b60ae7c7e8ce957fea42))
* remove testcase and scenario inputs to align with bash ([ff339ef](https://github.com/hamlet-io/engine-plugin-aws/commit/ff339efc824bbcec80b27b343d8d1bc770830a73))
* test and linting ([b0d7e86](https://github.com/hamlet-io/engine-plugin-aws/commit/b0d7e86d860330106c0c877163a885914a68e449))
* testing root dir location ([170ea45](https://github.com/hamlet-io/engine-plugin-aws/commit/170ea4556d5d506a7d071a3edfb93f875cb726c9))


### Features

* **deploy:** always appened end of line pattern ([646b4fe](https://github.com/hamlet-io/engine-plugin-aws/commit/646b4fe59fe18ede3ccd648df9e2268a96401429))
* add deploy command ([bb264cd](https://github.com/hamlet-io/engine-plugin-aws/commit/bb264cd72e2060d67448b2281051accd33f127b9))
* **schema:** add template level of schema for schema generation ([ae89c0d](https://github.com/hamlet-io/engine-plugin-aws/commit/ae89c0d12e30077db2ae9b2ca4be4236e81a7138))
* add create deployments and rework run deployments ([6279ee9](https://github.com/hamlet-io/engine-plugin-aws/commit/6279ee992a538a98499297a710d36f88c12778f9))
* add diagrams depdencies for visual ([#67](https://github.com/hamlet-io/engine-plugin-aws/issues/67)) ([cb6f945](https://github.com/hamlet-io/engine-plugin-aws/commit/cb6f945add04bc8c5887fae12f8401422a08c2c0))
* add schema level test ([c77521c](https://github.com/hamlet-io/engine-plugin-aws/commit/c77521c58dfbdb3d9d277f158578dd4a56d8125c))
* add support for diagram plugin generation and execution ([59d24d3](https://github.com/hamlet-io/engine-plugin-aws/commit/59d24d370cd0e2312e753d47178d3cb015a0a2cb))
* add support for entrances ([#55](https://github.com/hamlet-io/engine-plugin-aws/issues/55)) ([3e31422](https://github.com/hamlet-io/engine-plugin-aws/commit/3e3142276ff14e5e99f297fee672f6af4bb62b59))
* changelog generation ([#69](https://github.com/hamlet-io/engine-plugin-aws/issues/69)) ([ff7585f](https://github.com/hamlet-io/engine-plugin-aws/commit/ff7585fc573f8cd01b62ab747c2fdcdd6ead0f4d))
* filter list-deployments in line with commands ([90d8b82](https://github.com/hamlet-io/engine-plugin-aws/commit/90d8b82c96bab3176fb20e9edaec94d0ba544b2a))
* support additonal pytest arguments on run ([#52](https://github.com/hamlet-io/engine-plugin-aws/issues/52)) ([983508a](https://github.com/hamlet-io/engine-plugin-aws/commit/983508ab3ed7b1f55914d16a069f588b13a36f08))



# 7.0.0 (2020-03-20)



