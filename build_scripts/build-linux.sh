# modded from https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=zed-git
cargo fetch --locked --target "$(rustc -vV | sed -n 's/host: //p')"
export DO_STARTUP_NOTIFY="true"
export APP_ICON="zed"
export APP_NAME="Zed"
export APP_CLI=$_binname
envsubst < "crates/zed/resources/zed.desktop.in" > zed.desktop

patch -p0 -i ./use-lib-not-libexec.patch

export RUSTUP_TOOLCHAIN=stable
export CARGO_TARGET_DIR=target
export CFLAGS+=' -ffat-lto-objects'
export CXXFLAGS+=' -ffat-lto-objects'

export ZED_UPDATE_EXPLANATION='Updates are handled by pacman'
# cargo build --release --frozen --package zed --package cli

target_triple="$(rustc -vV | sed -n 's/host: //p')"
cargo build --release --target "${target_triple}" --package zed

strip --strip-debug "target/${target_triple}/release/zed"
