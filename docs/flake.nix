{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }: 
    let
      forAllSystems = nixpkgs.lib. genAttrs [ "x86_64-linux" "aarch64-linux" ];
    in {
      devShells = forAllSystems (system: 
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in {
          default = pkgs.mkShell {
            packages = with pkgs; [
              uv
              python312
            ];
            
            env = {
              UV_PYTHON_PREFERENCE = "only-system";
              UV_PYTHON = "${pkgs. python312}/bin/python";
            };
            
            NIX_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
              pkgs.stdenv.cc.cc
              pkgs.zlib
              pkgs.openssl
            ];
            NIX_LD = builtins.readFile "${pkgs.stdenv.cc}/nix-support/dynamic-linker";
            
            shellHook = ''
              export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH
              source .venv/bin/activate
              nvim 
            '';
          };
        }
      );
    };
}
