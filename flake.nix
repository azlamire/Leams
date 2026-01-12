{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
    let
      forAllSystems = nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" ];
    in {
      devShells = forAllSystems (system: 
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in {
          default = pkgs.mkShell {
            packages = with pkgs; [
              uv
              python312  # Use Nix-provided Python
            ];
            
            env = {
              # Tell uv to use system Python, not download its own
              UV_PYTHON_PREFERENCE = "only-system";
              UV_PYTHON = "${pkgs.python312}/bin/python";
            };
            
            shellHook = ''
              echo "🐍 Python:  $(python --version)"
              echo "📦 uv: $(uv --version)"
              echo ""
              echo "Usage:"
              echo "  uv init        # Initialize project"
              echo "  uv add <pkg>   # Add dependency"
              echo "  uv run <cmd>   # Run command"
            '';
          };
        }
      );
    };
}
