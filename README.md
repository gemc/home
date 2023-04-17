## Run from 'home' directory:

```
bundle exec jekyll serve
```

### Run Periodically:

(put all these in a single script please)
```
./scripts/periodic.sh
```

### Asciinema recording:

Remember to load the environment .

 ./asciinema-rec_script script_name.sh

asciinema upload script_name.sh.cast 

then login into asciinema.org to get the embed the player - add 

`data-autoplay="true" data-loop="true"`

when needed.

## To install [jekyll](https://jekyllrb.com):

It can be done with ruby. 
The ruby-install ruby can be skipped, can use brew to overwrite the old system version,
for example 

```
brew install ruby@3.0
brewDir=$(brew --prefix)
if [ -d $brewDir ]; then
	export PATH=$brewDir/opt/ruby@3.0/bin:$PATH
fi
```
 
 
```
brew install chruby ruby-install  
(sudo) gem install jekyll
```


---

- [ICONS](https://feathericons.com)
- [span tables and more](https://github.com/jeffreytse/jekyll-spaceship)

---

## Gist:

https://gist.github.com

## GH-PAGES

https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/creating-a-github-pages-site-with-jekyll

Remember to use the exact dependencies that are used on GitHub:

https://pages.github.com/versions/

Also remember to match the Gemfile plugins into the _config.yml

## Create a new site:

Follow the [jekyll tutorial](https://jekyllrb.com/docs/step-by-step/01-setup/).

At the editing the Gemfile step, add

gem "github-pages", "~> 227", group: :jekyll_plugins

check the [dependency versions](https://pages.github.com/versions/) 

May need to add [webrick](https://github.com/github/pages-gem/issues/752)

