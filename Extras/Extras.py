# def sum_f_y(points, segments_y):
#     ya, yb = symbols("ya yb")
#     forces_sum = 0
#     symbols_list = []
#     for point_x in points:
#         forces_sum += point_x.concentrated_forces
#         if point_x.support.name != "Free":
#             symbol_name = "y" + point_x.name
#             symbol_name = symbols(symbol_name)
#             symbols_list.append(symbol_name)
#         if point_x.support.name == "Fixed" or point_x.support.name == "Roller":
#             symbol_name = "m" + point_x.name
#             symbol_name = symbols(symbol_name)
#             symbols_list.append(symbol_name)
#     for segment in segments_y:
#         forces_sum += segment.distributed_force*segment.length
#     return Eq(sum(symbols_list), -1*forces_sum), symbols_list
