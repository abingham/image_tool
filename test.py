from image_tool.png import load, save
from image_tool.edge_detector import detect_edges, KIRSH, PREWITT

gs_pixels, width, height = load('llama.png')
save(gs_pixels, width, height, 'gs_llama.png')
gs_pixels, width, height = load('gs_llama.png')
edge_pixels = detect_edges(gs_pixels, height, width)
save(edge_pixels, width, height, 'edge_llama.png')
