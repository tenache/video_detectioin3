import colorsys

def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r*255), int(g*255), int(b*255))

def generate_color_sets(n_sets, n_colors_per_set):
    color_sets = []
    for i in range(n_sets):
        hue_start = i / float(n_sets)
        hue_end = (i + 1) / float(n_sets)
        hues = [hue_start + (hue_end - hue_start) * j / float(n_colors_per_set)
                for j in range(n_colors_per_set)]
        color_set_hsl = [(h, 0.5, 0.5) for h in hues]
        color_set_rgb = [hsl_to_rgb(*color) for color in color_set_hsl]
        color_sets.append(color_set_rgb)
    return color_sets

if __name__ == "__main__":
    print(generate_color_sets(2,10))
    
