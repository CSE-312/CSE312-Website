-- Quarto drops code-line-numbers="5-7,10" from the HTML page; keep the ranges
-- for line-highlight.html. Revealjs highlights them itself.
function CodeBlock(block)
  if quarto.doc.is_format("revealjs") then
    return nil
  end

  local lines = block.attributes["code-line-numbers"]
  if not lines or not lines:match("^[%d,|%-]+$") then
    return nil
  end

  block.attributes["highlight-lines"] = lines
  return block
end
