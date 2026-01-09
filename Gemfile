source "https://rubygems.org"

gem "jekyll", "~> 3.10.0"

# This is the default theme for new Jekyll sites. You may change this to anything you like.
gem "minima"
gem "base64"
gem "logger" # Add this proactively to avoid future errors with Ruby 3.5+
gem "csv", require: false
gem "bigdecimal", require: false
gem "webrick", "~> 1.8"


# If you have any plugins, put them here!
# admonitions: [!NOTE], [!TIP], [!WARNING], [!CAUTION], [!IMPORTANT]
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

# Performance booster for watching directories on Windows
gem "wdm", platforms: [:windows]

# kramdown v2 ships without the GFM parser by default
gem "kramdown-parser-gfm"

# (Optional) Let MRI/TruffleRuby use newer versions
gem "http_parser.rb", ">= 0.8", platforms: [:ruby, :truffleruby]
