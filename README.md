[![Push to Container Registry](https://github.com/bodo-hugo-barwich/rust-builder/actions/workflows/registry_upload.yml/badge.svg)](https://github.com/bodo-hugo-barwich/rust-builder/actions/workflows/registry_upload.yml)

# Rust-Builder
Docker Image with Rust Compiler in its `stable` version

## Features
* Additional Libraries for OpenSSL Web Development
* Non-`root` User Account
* Install Logs

## Toolchain Components
The **_Rust_ Toolchain Components** provided by this image can be found in the test results
in the test "_Show Environment and Compiler Version_":
```plain
* Operating System:
NAME="Ubuntu"
VERSION="16.04.7 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.7 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial
* Rust Compiler Version: 1.41.0
* RustUp Version:
rustup 1.26.0 (5af9b9484 2023-04-05)
info: This is the version for the rustup toolchain manager, not the rustc compiler.
info: The currently active `rustc` version is `rustc 1.41.0 (5e1a79984 2020-01-27)`
* RustUp Show:
Default host: x86_64-unknown-linux-gnu
rustup home:  /home/rust-build/.rustup

1.41.0-x86_64-unknown-linux-gnu (default)
rustc 1.41.0 (5e1a79984 2020-01-27)
* RustUp Toolchains Installed:
1.41.0-x86_64-unknown-linux-gnu (default)
* RustUp Components Installed:
cargo-x86_64-unknown-linux-gnu
clippy-x86_64-unknown-linux-gnu
rust-docs-x86_64-unknown-linux-gnu
rust-std-x86_64-unknown-linux-gnu
rustc-x86_64-unknown-linux-gnu
rustfmt-x86_64-unknown-linux-gnu
```

## Available Versions (Tags)
All available **_Rust_ Compiler Versions** are listed in the
_Version Matrix File_ `rust-version_matrix.yml`

New Versions can be added opening a **Pull Request** and adding the version to the
_Version Matrix File_

## Usage
The project directory will be mounted into the new container and be opened with `bash`
like:
```plain
$ docker pull ghcr.io/bodo-hugo-barwich/rust-builder:latest               # download the image or the desired Rust Version
$ docker run -v $(pwd):/home/rust-build/project/:Z -it rust-builder bash  # mount the project directory into the container
rust_builder@20ef08969521:~/project$ pwd
/home/rust-build/project                                                  # mounting point inside the container
rust_builder@20ef08969521:~/project$ ls -lah
total 100K
drwxr-xr-x 7 rust_builder rust 4.0K Mar 17  2022 .
drwxr-xr-x 1 rust_builder rust 4.0K Apr 15  2022 ..
drwxr-xr-x 7 rust_builder rust 4.0K Feb  2  2023 .git
drwxr-xr-x 3 rust_builder rust 4.0K Mar 14  2022 .github
-rw-r--r-- 1 rust_builder rust  110 Mar 10  2022 .gitignore
-rw-r--r-- 1 rust_builder rust  213 Mar 14  2022 .project
-rw-r--r-- 1 rust_builder rust  56K Mar 17  2022 Cargo.lock
-rw-r--r-- 1 rust_builder rust  608 Mar 17  2022 Cargo.toml
-rw-r--r-- 1 rust_builder rust 1.1K Mar 14  2022 README.md
drwxr-xr-x 4 rust_builder rust 4.0K Mar 17  2022 src
drwxr-xr-x 4 rust_builder rust 4.0K Mar 13  2022 target
drwxr-xr-x 2 rust_builder rust 4.0K Mar 17  2022 tests
rust_builder@20ef08969521:~/project$ rustup show
Default host: x86_64-unknown-linux-gnu
rustup home:  /home/rust-build/.rustup

stable-x86_64-unknown-linux-gnu (default)
rustc 1.60.0 (7737e0b5c 2022-04-04)
rust_builder@20ef08969521:~/project$ cargo test                           # run the 'cargo' commands as usual
    Updating crates.io index
  Downloaded actix-macros v0.1.3
  // ...
   Compiling actix-web v3.3.3
   Compiling alerting_email v0.0.1 (/home/rust-build/project)
    Finished test [unoptimized + debuginfo] target(s) in 11m 53s
     Running unittests (target/debug/deps/alerting_email-d18154a3163a817d)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests (target/debug/deps/grafana_alerting_email-80e557f97ac92548)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running tests/integration_tests.rs (target/debug/deps/integration_tests-69422124e8eb7ebf)

running 3 tests
test tests::test_ping ... ok
test tests::test_send ... ok
test tests::test_home ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests alerting_email

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

```

### Build Artifacts
The build artifacts are placed in the target directory of the Docker Host


