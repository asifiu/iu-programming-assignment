from bokeh.layouts import column
from bokeh.models import HoverTool
from bokeh.plotting import figure, show, output_file


def plot_results(train_df, ideal_df, test_df, mapped_df, chosen_functions):
    """
    Create Bokeh visualizations
    """
    output_file("results.html")
    plots = []
    
    colors = ['blue', 'green', 'red', 'purple']
    
    # Training vs ideal function plots
    for i, (train_col, ideal_col) in enumerate(chosen_functions.items()):
        p = figure(title=f"{train_col} vs {ideal_col}", 
                  x_axis_label='x', y_axis_label='y',
                  width=800, height=400)
        
        p.line(train_df['x'], train_df[train_col],
              legend_label=f'Training {train_col}',
              color=colors[i], line_dash='dashed', line_width=2)
        
        p.line(ideal_df['x'], ideal_df[ideal_col],
              legend_label=f'Ideal {ideal_col}',
              color=colors[i], line_width=2)
        
        p.legend.click_policy = "hide"
        plots.append(p)
    
    # Test data mapping plot
    p = figure(title="Test Data Mapping",
              x_axis_label='x', y_axis_label='y',
              width=1200, height=500)
    
    # Unmapped points
    if not mapped_df.empty:
        mapped_coords = set(zip(mapped_df['x'], mapped_df['y']))
        unmapped = test_df[~test_df.apply(
            lambda row: (row['x'], row['y']) in mapped_coords, axis=1)]
        
        if not unmapped.empty:
            p.scatter(unmapped['x'], unmapped['y'],
                    size=6, color='gray', alpha=0.5,
                    legend_label=f'Unmapped ({len(unmapped)})')
    
    # Mapped points with color coding
    if not mapped_df.empty:
        max_dev = mapped_df['delta_y'].max()
        
        def get_color(dev):
            if dev < max_dev * 0.33:
                return 'green'
            elif dev < max_dev * 0.67:
                return 'orange'
            return 'red'
        
        mapped_df['color'] = mapped_df['delta_y'].apply(get_color)
        
        hover = HoverTool(tooltips=[
            ("X", "@x{0.00}"),
            ("Y", "@y{0.00}"),
            ("Deviation", "@delta_y{0.0000}"),
            ("Function", "@function_id")
        ])
        p.add_tools(hover)
        
        p.scatter('x', 'y', size=8, color='color', alpha=0.8,
                legend_label=f'Mapped ({len(mapped_df)})',
                source={'x': mapped_df['x'], 'y': mapped_df['y'],
                       'delta_y': mapped_df['delta_y'],
                       'function_id': mapped_df['function_id'],
                       'color': mapped_df['color']})
    p.legend.click_policy = "hide"
    plots.append(p)
    
    show(column(*plots))
    print("Visualization saved to results.html")
