module Jekyll
  module ReadFileFilter
    def read_file(input)
      file_path = File.expand_path(input, Dir.pwd)  # Resolves path relative to project root
      # Log the resolved file path
      Jekyll.logger.info "Attempting to read file from: #{file_path}"

      if File.exist?(file_path)
        begin
          # Attempt to read the file content
          file_content = File.read(file_path)

          # Log the content to ensure it’s being read
          Jekyll.logger.info "File content read successfully."
          Jekyll.logger.debug "Content: #{file_content}"

          # Return the content to Liquid
          file_content
        rescue => e
          # Log any errors encountered while reading
          Jekyll.logger.error "Error reading file: #{e.message}"
          "Error reading file: #{e.message}"
        end
      else
        # Log if the file doesn’t exist
        Jekyll.logger.error "File not found: #{file_path}"
        "File not found: #{input}"
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::ReadFileFilter)
