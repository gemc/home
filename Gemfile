source "https://rubygems.org"
# Hello! This is where you manage which Jekyll version is used to run.
# When you want to use a different version, change it below, save the
# file and run `bundle install`. Run Jekyll with `bundle exec`, like so:
#
#     bundle exec jekyll serve
#
# gem "jekyll", "~> 3.10.0"

# minima seems too old
#gem "minimal-mistakes-jekyll"
gem "minima"

# If you want to use GitHub Pages, remove the "gem "jekyll"" above and
# uncomment the line below. To upgrade, run `bundle update github-pages`.
gem "github-pages", group: :jekyll_plugins

# If you have any plugins, put them here!
group :jekyll_plugins do
	gem "jekyll-feed"
 	gem "jekyll-gfm-admonitions"
	gem "jekyll-toc"
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :windows, :jruby do
  gem "tzinfo"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", :platforms => [:windows]

# kramdown v2 ships without the gfm parser by default.
gem "kramdown-parser-gfm"

# Lock to the last JRuby-compatible line (Java impl was dropped after 0.6.x)
# gem "http_parser.rb", "~> 0.6", platforms: :jruby

# (Optional) Let MRI/TruffleRuby use newer versions
gem "http_parser.rb", ">= 0.8", platforms: [:ruby, :truffleruby]
