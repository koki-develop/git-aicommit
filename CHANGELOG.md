# Changelog

## [0.5.1](https://github.com/koki-develop/git-aicommit/compare/v0.5.0...v0.5.1) (2025-11-19)


### Patches

* clarify commit message body formatting guideline ([a57f1a4](https://github.com/koki-develop/git-aicommit/commit/a57f1a4e43803c7815cf70bdea6068f041c2bbe1))

## [0.5.0](https://github.com/koki-develop/git-aicommit/compare/v0.4.0...v0.5.0) (2025-11-18)


### Features

* add `init` subcommand for config file generation ([#21](https://github.com/koki-develop/git-aicommit/issues/21)) ([1147a83](https://github.com/koki-develop/git-aicommit/commit/1147a837c419fdcd6456c6e0ff64ee4c71cadf0b))


### Patches

* centralize CLI error handling and improve config errors ([#23](https://github.com/koki-develop/git-aicommit/issues/23)) ([d131f63](https://github.com/koki-develop/git-aicommit/commit/d131f63b18f7b0d782101e529921a58c79ee792d))

## [0.4.0](https://github.com/koki-develop/git-aicommit/compare/v0.3.0...v0.4.0) (2025-11-18)


### Features

* add Amazon Bedrock provider support ([#20](https://github.com/koki-develop/git-aicommit/issues/20)) ([a665604](https://github.com/koki-develop/git-aicommit/commit/a66560497a64128a9b9ba99dfc5d1534b40c00dd))
* add Anthropic provider support ([#19](https://github.com/koki-develop/git-aicommit/issues/19)) ([d34288f](https://github.com/koki-develop/git-aicommit/commit/d34288f41c670a42d308df8bae7d2cdd55226331))


### Patches

* switch config keys to kebab-case ([#17](https://github.com/koki-develop/git-aicommit/issues/17)) ([4774b49](https://github.com/koki-develop/git-aicommit/commit/4774b49ae097dcfd8d90bcc6f602d3139d798c52))

## [0.3.0](https://github.com/koki-develop/git-aicommit/compare/v0.2.0...v0.3.0) (2025-11-18)


### Features

* Support Google Generative AI ([#16](https://github.com/koki-develop/git-aicommit/issues/16)) ([c23efa2](https://github.com/koki-develop/git-aicommit/commit/c23efa25cf7e1938fff5253e7238f1508473d9aa))


### Patches

* clarify example in AI prompt guideline for style conventions ([3a96ef1](https://github.com/koki-develop/git-aicommit/commit/3a96ef18496bda27ef2abe4ae1230e7d9e7e808b))
* update AI prompt to include detailed persona, objectives, and guidelines for generating precise commit messages ([1f54ea7](https://github.com/koki-develop/git-aicommit/commit/1f54ea7d919da1eb4e77efb018bc6e106cd9f757))

## [0.2.0](https://github.com/koki-develop/git-aicommit/compare/v0.1.1...v0.2.0) (2025-11-18)


### Features

* Support OpenAI Provider ([#14](https://github.com/koki-develop/git-aicommit/issues/14)) ([35028d4](https://github.com/koki-develop/git-aicommit/commit/35028d4329d81992939157872d06aee2cae3cccb))


### Documentation

* Update readme ([965f5dd](https://github.com/koki-develop/git-aicommit/commit/965f5dd97e1fd92679dd1e2960d005942c9e2ed6))

## 0.1.1 (2025-11-17)


### Features

* **cli:** add command‑line interface for AI‑generated commit messages ([75ae69b](https://github.com/koki-develop/git-aicommit/commit/75ae69b2ac96a91f6a6c687035e0af02b9bb1cf2))
* **cli:** add halo spinners for message generation and commit ([356ad69](https://github.com/koki-develop/git-aicommit/commit/356ad69c12f23117947a86ccb2ec2f22c09de059))
* **cli:** add key‑based commit confirmation and feedback loop ([b01315a](https://github.com/koki-develop/git-aicommit/commit/b01315a9312ed552cdecdad2d13c831a5c4cab33))
* Release v0.0.1 ([4487292](https://github.com/koki-develop/git-aicommit/commit/4487292e97fc94d28b61f6aa568e99032b9ed5dd))
* Release v0.0.2 ([8196ce5](https://github.com/koki-develop/git-aicommit/commit/8196ce5766e7070a222c50b620cff92aab7ad335))
* Release v0.0.3 ([bb2459a](https://github.com/koki-develop/git-aicommit/commit/bb2459a86c07875d1a5e11c4c2c32fc03ece6d83))
* Release v0.1.0 ([3187290](https://github.com/koki-develop/git-aicommit/commit/3187290e63039cecd4f6a49f5f0a916aa9f06a44))
* Release v0.1.1 ([8e5e85a](https://github.com/koki-develop/git-aicommit/commit/8e5e85aaa725cb18bdf16c9bfee8ccbfff615fb7))


### Bug Fixes

* **cli:** add AbortCommitError for cleaner abort handling ([1e83383](https://github.com/koki-develop/git-aicommit/commit/1e83383d1af39d776579db2ac4f79af2e3f0e550))
* **cli:** add header to preview message ([4e1e499](https://github.com/koki-develop/git-aicommit/commit/4e1e4990d8d93d16aa59259d01cab099443c6170))
* **cli:** add version flag and help description to git‑aicommit command ([ca4b8bf](https://github.com/koki-develop/git-aicommit/commit/ca4b8bf367c4173dcd40ef3f28674cbd4dde521a))
* **cli:** update feedback prompt to bold style ([5f93768](https://github.com/koki-develop/git-aicommit/commit/5f937688bbc2f6d36faf6590e8033d51bbad57aa))
* remove poml dependency and related imports ([2b25b0d](https://github.com/koki-develop/git-aicommit/commit/2b25b0d43a37b537abf1e6e431b081d14235e398))
* use git CLI for commit instead of index.commit ([3d53b49](https://github.com/koki-develop/git-aicommit/commit/3d53b4901a5110a7481a4527ab08b3bbcbe6225e))


### Documentation

* add badges, installation and usage instructions to README ([abc265f](https://github.com/koki-develop/git-aicommit/commit/abc265f3027f06eecef0f493a1b429034309c845))
* add CLAUDE.md with project overview, architecture, and usage instructions ([0147819](https://github.com/koki-develop/git-aicommit/commit/0147819a1775be3600126549d9234603f19f7039))
* add comment explaining why git CLI is used for commits (signing support) ([a3ba223](https://github.com/koki-develop/git-aicommit/commit/a3ba223a869179d3248d4ed5e0912e2ebcd86a5a))
* Add MIT License to the project ([4325f7d](https://github.com/koki-develop/git-aicommit/commit/4325f7d93576207fdff0c3778b5d38ee29281d47))
* Create readme ([e9f9956](https://github.com/koki-develop/git-aicommit/commit/e9f995671d107e760354fcc994278f0070c1a435))
