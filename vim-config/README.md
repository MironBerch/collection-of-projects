# nvim config
### Install dependencies
- `sudo apt update`- update  packages
- `sudo apt install nodejs` - install node js
- `sudo npm install -g npm@latest` - install last npm version
- `sudo apt install neovim` - install nvim
- `mkdir -p ~/.local/share/nvim/site/autoload/` - make dir for plugins

### Install vim plug 
For unix linux
```sh
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs \
       https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
```
If does not work
```sh
curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```
For windows
```powershell
iwr -useb https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim |`
    ni "$(@($env:XDG_DATA_HOME, $env:LOCALAPPDATA)[$null -eq $env:XDG_DATA_HOME])/nvim-data/site/autoload/plug.vim" -Force
```

### Install Plugs
`:PlugInstall` - run it in nvim command line

