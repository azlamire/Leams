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
              # Docker, watchexec, envsubst are vital for this project

              # docker for conterization and handy local/deploy usage
              docker
              # https://www.docker.com/

              # watchexec for watching the file if it's changed it used in Makefile
              watchexec
              # https://github.com/watchexec/watchexec

              # envsubst for replacing ${} env varaibles where it can't be like compose.yaml or .envs.
              # used in Makefile with watchexec
              envsubst

              # uv very handy for python implementation it contains a lot like poetry pip python and so on
              uv
              # https://docs.astral.sh/uv/
              
              # ssh that mount to your filesystem and you can control vps from your pc it includes also IDE 
              # sshfs
              # https://github.com/winfsp/sshfs-win
              
              # act for testing and making ci/cd. Githu actions but local
              # act
              # https://github.com/nektos/act

              # openssl for making selfsigned key and certificates for https. It's local usually
              # openssl
              # https://github.com/openssl/openssl
              
              # nging reverse proxy server
              # nginx
              # https://nginx.org/en/
            ];
          };
        }
      );
    };
}
