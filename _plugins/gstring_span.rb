# frozen_string_literal: true

# _plugins/gstring_span.rb
#
# Converts:
#
#   %%G4Box%%
#
# into:
#
#   <span class="gstring">G4Box</span>
#
# Safe behavior:
# - Does not touch inline code in backticks:
#     `FTFP_BERT + G4OpticalPhysics`
# - Does not touch fenced code blocks:
#     ```yaml
#     physics: FTFP_BERT + G4OpticalPhysics
#     ```
# - Does not touch Liquid raw blocks.
# - Escapes HTML inside %%...%%.
# - Allows literal delimiters with \%%.

require "cgi"

module Jekyll
  module GStringSpanPlugin
    GSTRING_PATTERN = /(?<!\\)%%([^\n]*?)(?<!\\)%%/.freeze
    ESCAPED_DELIMITER_PATTERN = /\\%%/.freeze

    RAW_START_PATTERN = /\{%\s*raw\s*%\}/.freeze
    RAW_END_PATTERN = /\{%\s*endraw\s*%\}/.freeze
    FENCE_START_PATTERN = /\A[ \t]*(`{3,}|~{3,})/.freeze

    def self.convert(content)
      output = +""

      in_fenced_code = false
      fence_char = nil
      fence_length = 0
      in_raw_block = false

      content.each_line do |line|
        if in_raw_block
          output << line
          in_raw_block = false if line.match?(RAW_END_PATTERN)
          next
        end

        if line.match?(RAW_START_PATTERN)
          output << line
          in_raw_block = true unless line.match?(RAW_END_PATTERN)
          next
        end

        if in_fenced_code
          output << line

          if closing_fence?(line, fence_char, fence_length)
            in_fenced_code = false
            fence_char = nil
            fence_length = 0
          end

          next
        end

        fence_match = line.match(FENCE_START_PATTERN)

        if fence_match
          fence = fence_match[1]
          in_fenced_code = true
          fence_char = fence[0]
          fence_length = fence.length
          output << line
          next
        end

        output << convert_line_outside_inline_code(line)
      end

      output
    end

    def self.closing_fence?(line, fence_char, fence_length)
      return false unless fence_char
      return false unless fence_length.positive?

      pattern = /\A[ \t]*#{Regexp.escape(fence_char)}{#{fence_length},}[ \t]*\r?\n?\z/
      line.match?(pattern)
    end

    def self.convert_line_outside_inline_code(line)
      result = +""
      normal_text = +""
      i = 0

      while i < line.length
        if line[i] == "`"
          result << convert_gstrings(normal_text)
          normal_text.clear

          tick_start = i
          tick_end = i

          tick_end += 1 while tick_end < line.length && line[tick_end] == "`"

          tick_sequence = line[tick_start...tick_end]
          closing_index = line.index(tick_sequence, tick_end)

          if closing_index
            result << line[tick_start...(closing_index + tick_sequence.length)]
            i = closing_index + tick_sequence.length
          else
            result << line[tick_start..]
            return result
          end
        else
          normal_text << line[i]
          i += 1
        end
      end

      result << convert_gstrings(normal_text)
      result
    end

    def self.convert_gstrings(text)
      text
        .gsub(GSTRING_PATTERN) do
          inner_text = Regexp.last_match(1)
          inner_text = inner_text.gsub(ESCAPED_DELIMITER_PATTERN, "%%")

          %(<span class="gstring">#{CGI.escapeHTML(inner_text)}</span>)
        end
        .gsub(ESCAPED_DELIMITER_PATTERN, "%%")
    end
  end
end

Jekyll::Hooks.register [:pages, :documents], :pre_render do |doc|
  next unless doc.respond_to?(:extname)
  next unless doc.extname.match?(/\.(md|markdown)$/i)

  doc.content = Jekyll::GStringSpanPlugin.convert(doc.content)
end