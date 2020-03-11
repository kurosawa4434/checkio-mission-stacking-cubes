//Dont change it
requirejs(['ext_editor_io', 'jquery_190', 'raphael_210'],
    function (extIO, $) {
        function stackingCubesAnimation(tgt_node, data) {

            if (!data || !data.ext) {
                return
            }

            const input = data.in
            const explanation = data.ext.explanation

            /*----------------------------------------------*
            *
            * attr
            *
            *----------------------------------------------*/
            const attr = {
                cube: {
                    blue: {
                        dark: {
                            'stroke-width': 0.5,
                            'stroke-width': 0,
                            'fill': '#0E81B3',
                        },
                        mid: {
                            'stroke-width': 0.5,
                            'stroke-width': 0,
                            'fill': '#38B8EE',
                        },
                        light: {
                            'stroke-width': 0.5,
                            'stroke-width': 0,
                            'fill': '#68C9F2',
                        },
                    },
                    orange: {
                        dark: {
                            'stroke-width': 0.5,
                            'stroke-width': 0,
                            'fill': '#F0801A',
                        },
                        mid: {
                            'stroke-width': 0.5,
                            'stroke-width': 0,
                            'fill': '#F4A561',
                        },
                        light: {
                            'stroke-width': 0.5,
                            'stroke-width': 0,
                            'fill': '#F7C091',
                        },
                    },
                },
                axis: {
                    normal: {
                        'stroke-width': '0.6px',
                        'stroke': '#294270',
                    },
                    arrow_end: {
                        'stroke-width': '0.6px',
                        'stroke': '#294270',
                        'arrow-end': 'block-wide-long',
                    },
                },
            };

            /*----------------------------------------------*
            *
            * values
            *
            *----------------------------------------------*/
            const EDGE = 13

            /*----------------------------------------------*
            *
            * paper
            *
            *----------------------------------------------*/
            let max_coord = 10
            let sizes = []
            let bottoms = []
            const height = EDGE / 2
            const base = (EDGE / 2) * Math.sqrt(3)
            explanation.forEach(([x, y, h]) => {
                max_coord = Math.max(...[max_coord, x, x + 1, h, h + 1, y, y + 1].map(c => Math.abs(c)))
                const left = (x * base) + (y * base)
                const right = left + base * 2
                const bottom = (x * height) + (y * -height) + (h * -EDGE) + height
                const top = bottom - EDGE * 2
                sizes = sizes.concat([left, right, top].map(c => Math.abs(c)))
                // bottoms = bottoms.concat([bottom].map(c => Math.abs(c)))
                bottoms.push(bottom)
            })

            const max_px_size = Math.max(...sizes.concat([EDGE * Math.max(12, max_coord*1.1)]))
            const max_px_bottom_size = Math.max(...bottoms, ([EDGE/2 * Math.max(12, max_coord * 1.2)]))

            const SCALE = EDGE * 12 / max_px_size
            const OFFSET = max_px_size * SCALE

            const paper_width = max_px_size * 2 * SCALE
            const paper_height = (max_px_size + max_px_bottom_size) * SCALE
            // const paper_height = (max_px_size) * SCALE

            const paper = Raphael(tgt_node, paper_width, paper_height, 0, 0)

            /*----------------------------------------------*
            *
            * draw process
            *
            *----------------------------------------------*/
            const axis_units = [['origin', -1, -1, 0]]

            for (let i = -(max_coord + 1); i <= max_coord; i += 1) {
                axis_units.push(['x_axis', i, 0, 0])
                axis_units.push(['y_axis', 0, i, 0])
                if (i >= 0) {
                    axis_units.push(['height', 0, 0, i])
                }
            }

            const cubes = explanation.map(inp=>['orange', ...inp])

            const all_cubes = [
                ...axis_units,
                ...cubes,
            ].sort(sort_cubes)

            for (let cube of all_cubes) {
                draw_cube(...cube)
            }

            /*----------------------------------------------*
            *
            * sort cubes
            *
            *----------------------------------------------*/
            function sort_cubes(a, b) {
                const [ac, ax, ay, ah, ae] = a
                const [bc, bx, by, bh, be] = b
                if (ah > bh) return 1
                if (ah < bh) return -1
                if (ax > bx) return 1
                if (ax < bx) return -1
                if (ay < by) return 1
                if (ay > by) return -1
                return 0
            }

            /*----------------------------------------------*
            *
            * draw cube (and axis)
            *
            *----------------------------------------------*/
            function draw_cube(color, cx, cy, ch, top, left, right) {

                const edge = EDGE * SCALE
                const height = edge / 2
                const base = (edge / 2) * Math.sqrt(3)

                const x = (cx * base) + (cy * base) + OFFSET
                const y = (cx * height) + (cy * -height) + (ch * -edge) + OFFSET

                if (color == 'origin') {
                    paper.text(max_px_size * SCALE, max_px_size * SCALE + 10, 0)

                } else if (color == 'height') {
                    paper.path(['M', x, y, 'v', -edge]).attr(
                        ch == max_coord ? attr.axis.arrow_end : attr.axis.normal)
                    if (ch == max_coord) {
                        paper.text(x - 7, y - edge, 'height').attr({'text-anchor': 'end', 'font-size': 10 })
                    }

                } else if (color == 'x_axis') {
                    paper.path(['M', x, y, 'l', base, height]).attr(
                        cx == max_coord ? attr.axis.arrow_end : attr.axis.normal)
                    if (cx == max_coord) {
                        paper.text(x + base, y + height - 8, 'x').attr({ 'font-size': 10 })
                    }

                } else if (color == 'y_axis') {
                    paper.path(['M', x, y, 'l', base, -height]).attr(
                        cy == max_coord ? attr.axis.arrow_end : attr.axis.normal)
                    if (cy == max_coord) {
                        paper.text(x + base, y - height - 8, 'y').attr({ 'font-size': 10 })
                    }

                } else {
                    // draw cube

                    // top
                    if (top) {
                        paper.path(['M', x, y - edge,
                            'l', base, -height,
                            'l', base, height,
                            'l', -base, height, 'z']).attr(attr.cube[color].mid)
                    }

                    // left
                    if (left) {
                        paper.path(['M', x, y,
                            'v', -edge,
                            'l', base, height,
                            'v', edge, 'z']).attr(attr.cube[color].light)
                    }

                    // right
                    if (right) {
                        paper.path(['M', x + base, y + height,
                            'l', base, -height,
                            'v', -edge,
                            'l', -base, height, 'z']).attr(attr.cube[color].dark)
                    }
                }
            }
        }

        var $tryit;

        var io = new extIO({
            multipleArguments: false,
            functions: {
                python: 'stacking_cubes',
                js: 'stackingCubes'
            },
            animation: function ($expl, data) {
                stackingCubesAnimation(
                    $expl[0],
                    data,
                );
            }
        });
        io.start();
    }
);
