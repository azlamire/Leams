{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    
    # FIX 1: Removed the extra "inputs." prefix here
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { nixpkgs, pyproject-nix, ... }: 
    let
      # FIX 2: Removed accidental space in "lib. genAttrs"
      forAllSystems = nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" ];
    in {
      devShells = forAllSystems (system: 
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python3;
          
          project = pyproject-nix.lib.project.loadPyproject {
            projectRoot = ./.;
          };
          
          attrs = project.renderers.buildPythonPackage { inherit python; };
        in {
          default = pkgs.mkShell {
            packages = with pkgs; [
              uv 
              chromium
              protonmail-bridge
              cloudflare-cli
              # (python.pkgs.buildPythonPackage attrs)
            ];
          };
        }
      );
    };
}
