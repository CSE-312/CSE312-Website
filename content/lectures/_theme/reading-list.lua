
local function inlines(value)
  if type(value) == "string" then
    return { pandoc.Str(value) }
  end
  return pandoc.utils.blocks_to_inlines({ pandoc.Plain(value) })
end

function Pandoc(doc)
  local entries = doc.meta["reading-list"]
  if not entries or #entries == 0 then
    return nil
  end

  local items = {}
  for _, entry in ipairs(entries) do
    local url = pandoc.utils.stringify(entry.url)
    local label = entry.text and inlines(entry.text) or { pandoc.Str(url) }
    items[#items + 1] = { pandoc.Plain({ pandoc.Link(label, url) }) }
  end

  local blocks = doc.blocks
  blocks:insert(pandoc.Header(2, { pandoc.Str("Further"), pandoc.Space(), pandoc.Str("Reading") },
    pandoc.Attr("further-reading")))
  blocks:insert(pandoc.BulletList(items))

  return pandoc.Pandoc(blocks, doc.meta)
end
