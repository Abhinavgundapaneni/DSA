"""
Manim Animation Script: AGR-002 - Max Flow With Vertex Capacities
Production-quality, Zero-Overlap animation following Universal Manim DSA Prompt v2.0

Topic: Advanced Graphs - Max Flow with Vertex Splitting Technique

Run command: manim -pql AGR-002-max-flow-vertex-capacity.py AGR002MaxFlowScene
For high quality: manim -pqh AGR-002-max-flow-vertex-capacity.py AGR002MaxFlowScene
"""

from manim import *
import numpy as np

# Color Palette
SUCCESS_GREEN = GREEN
ERROR_RED = RED
ACTIVE_BLUE = BLUE
HIGHLIGHT_YELLOW = YELLOW
RESULT_TEAL = TEAL
NODE_DEFAULT = WHITE
EDGE_DEFAULT = GRAY
VERTEX_IN = PURPLE
VERTEX_OUT = ORANGE
FLOW_COLOR = BLUE_C


class AGR002MaxFlowScene(Scene):
    """
    Complete animation for Max Flow with Vertex Capacities problem.
    Follows Strict Sequential Flow - Zero Overlap Design Philosophy.
    """

    def construct(self):
        """Main animation orchestrator"""
        self.scene_1_intro()
        self.scene_2_problem()
        self.scene_3_real_world_analogy()
        self.scene_4_vertex_capacity_concept()
        self.scene_5_naive_approach()
        self.scene_6_epiphany()
        self.scene_7_vertex_splitting_technique()
        self.scene_8_transformation_example()
        self.scene_9_dry_run_input()
        self.scene_10_dry_run_split()
        self.scene_11_max_flow_result()
        self.scene_12_complexity()
        self.scene_13_conclusion()

    def clear_screen(self):
        """Helper to clear all mobjects"""
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(0.3)

    # =========================================================================
    # SCENE 1: INTRO
    # =========================================================================
    def scene_1_intro(self):
        """Introduction"""
        title = Text("AGR-002: Max Flow With Vertex Capacities", font_size=38, color=ACTIVE_BLUE)
        title.move_to(ORIGIN)
        self.play(Write(title), run_time=2)
        self.wait(2.5)
        self.play(FadeOut(title))

        topic = Text("Advanced Graph Algorithm", font_size=36, color=HIGHLIGHT_YELLOW)
        topic.move_to(ORIGIN)
        self.play(FadeIn(topic))
        self.wait(2)
        self.play(FadeOut(topic))

        technique = Text("Vertex Splitting + Dinic's Algorithm", font_size=38, color=SUCCESS_GREEN)
        technique.move_to(ORIGIN)
        self.play(Write(technique))
        self.wait(2.5)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 2: PROBLEM STATEMENT
    # =========================================================================
    def scene_2_problem(self):
        """Given vs Goal"""
        # GIVEN
        given_title = Text("GIVEN:", font_size=36, color=ACTIVE_BLUE)
        given_title.move_to(UP * 2)
        self.play(Write(given_title))
        self.wait(0.5)

        given_items = VGroup(
            Text("• Directed graph with EDGE capacities", font_size=28),
            Text("• VERTEX capacities (limit flow through node)", font_size=28),
            Text("• Source node s and sink node t", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        given_items.next_to(given_title, DOWN, buff=0.6)
        
        for item in given_items:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.7)
            self.wait(0.5)
        self.wait(1.5)
        
        self.play(FadeOut(given_title), FadeOut(given_items))
        self.wait(0.3)

        # GOAL
        goal_title = Text("GOAL:", font_size=36, color=SUCCESS_GREEN)
        goal_title.move_to(UP * 2)
        self.play(Write(goal_title))
        self.wait(0.5)

        goal_items = VGroup(
            Text("• Compute maximum flow from s to t", font_size=28),
            Text("• Respect BOTH edge and vertex limits", font_size=28),
            Text("• Source and sink have unlimited capacity", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        goal_items.next_to(goal_title, DOWN, buff=0.6)
        
        for item in goal_items:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.7)
            self.wait(0.5)
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 3: REAL-WORLD ANALOGY
    # =========================================================================
    def scene_3_real_world_analogy(self):
        """Airport passenger throughput"""
        title = Text("Real-World: Airport Passenger Throughput", font_size=30, color=HIGHLIGHT_YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1.5)
        self.play(FadeOut(title))

        # Create simple airport network
        positions = {
            "NYC": LEFT * 3,
            "London": ORIGIN,
            "Paris": RIGHT * 3,
        }
        
        airports = VGroup()
        labels_text = ["NYC\n∞", "London\nCap: 500/hr", "Paris\n∞"]
        
        for i, (name, label_text) in enumerate(zip(["NYC", "London", "Paris"], labels_text)):
            if name == "London":
                color = HIGHLIGHT_YELLOW
            else:
                color = ACTIVE_BLUE
            circle = Circle(radius=0.6, color=color, fill_opacity=0.3, stroke_width=3)
            circle.move_to(positions[name])
            label = Text(label_text, font_size=18, color=WHITE)
            label.move_to(positions[name])
            airports.add(VGroup(circle, label))
        
        self.play(Create(airports), run_time=1.5)
        self.wait(1)

        # Flights (edges)
        edges_info = [
            (positions["NYC"], positions["London"], "Flight: 800 seats"),
            (positions["London"], positions["Paris"], "Flight: 700 seats"),
        ]
        
        edges = VGroup()
        for start, end, label_text in edges_info:
            arrow = Arrow(start + RIGHT * 0.6, end + LEFT * 0.6, color=EDGE_DEFAULT, stroke_width=3, buff=0)
            edges.add(arrow)
            mid = (start + end) / 2
            label = Text(label_text, font_size=16, color=HIGHLIGHT_YELLOW)
            label.next_to(mid, UP, buff=0.2)
            edges.add(label)
        
        self.play(Create(edges), run_time=1.5)
        self.wait(1.5)

        # Explanation
        exp = VGroup(
            Text("Even with 800 seats from NYC,", font_size=22, color=WHITE),
            Text("London airport can only process 500 passengers/hr", font_size=22, color=ERROR_RED),
            Text("→ Bottleneck: Vertex capacity!", font_size=22, color=HIGHLIGHT_YELLOW),
        ).arrange(DOWN, buff=0.3)
        exp.to_edge(DOWN, buff=0.5)
        
        for e in exp:
            self.play(FadeIn(e), run_time=0.6)
            self.wait(0.8)
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 4: VERTEX CAPACITY CONCEPT
    # =========================================================================
    def scene_4_vertex_capacity_concept(self):
        """Explain what vertex capacity means"""
        title = Text("What is Vertex Capacity?", font_size=36, color=ACTIVE_BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # Simple example
        node = Circle(radius=0.6, color=HIGHLIGHT_YELLOW, fill_opacity=0.3, stroke_width=3)
        node.move_to(ORIGIN)
        node_label = Text("B\nCap = 5", font_size=22, color=WHITE)
        node_label.move_to(ORIGIN)
        
        self.play(Create(node), Write(node_label))
        self.wait(1)

        # Incoming edges
        left_pos = LEFT * 3
        incoming1 = Arrow(left_pos + UP, node.get_left() + UP * 0.3, color=FLOW_COLOR, stroke_width=4, buff=0.1)
        incoming2 = Arrow(left_pos + DOWN, node.get_left() + DOWN * 0.3, color=FLOW_COLOR, stroke_width=4, buff=0.1)
        in_label1 = Text("10", font_size=18, color=HIGHLIGHT_YELLOW).next_to(incoming1, UP, buff=0.1)
        in_label2 = Text("10", font_size=18, color=HIGHLIGHT_YELLOW).next_to(incoming2, DOWN, buff=0.1)
        
        self.play(Create(incoming1), Create(incoming2), Write(in_label1), Write(in_label2))
        self.wait(1)

        # Outgoing edge
        right_pos = RIGHT * 3
        outgoing = Arrow(node.get_right(), right_pos, color=FLOW_COLOR, stroke_width=4, buff=0.1)
        out_label = Text("?", font_size=20, color=ERROR_RED).next_to(outgoing, UP, buff=0.1)
        
        self.play(Create(outgoing), Write(out_label))
        self.wait(1)

        # Explanation
        exp1 = Text("Total incoming: 10 + 10 = 20 units", font_size=24, color=WHITE)
        exp1.to_edge(DOWN, buff=1.5)
        self.play(Write(exp1))
        self.wait(1.5)
        self.play(FadeOut(exp1))

        exp2 = Text("But node B can only process 5 units!", font_size=24, color=ERROR_RED)
        exp2.to_edge(DOWN, buff=1.5)
        self.play(Write(exp2))
        self.wait(1)
        
        self.play(Transform(out_label, Text("5", font_size=20, color=SUCCESS_GREEN).next_to(outgoing, UP, buff=0.1)))
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 5: NAIVE APPROACH
    # =========================================================================
    def scene_5_naive_approach(self):
        """Naive approach"""
        title = Text("Naive Approach", font_size=36, color=ERROR_RED)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        idea = VGroup(
            Text("Modify Max Flow algorithm to track", font_size=26),
            Text("vertex usage separately", font_size=26),
        ).arrange(DOWN, buff=0.3)
        idea.move_to(ORIGIN + UP * 0.5)
        
        for i in idea:
            self.play(FadeIn(i), run_time=0.7)
            self.wait(0.6)
        self.wait(1)
        self.play(FadeOut(idea))

        problems = VGroup(
            Text("⚠️ Problems:", font_size=28, color=ERROR_RED),
            Text("• Complex to implement correctly", font_size=24),
            Text("• Error-prone bookkeeping", font_size=24),
            Text("• Hard to debug", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        problems.move_to(ORIGIN)
        
        self.play(FadeIn(problems[0]))
        self.wait(0.5)
        for p in problems[1:]:
            self.play(FadeIn(p, shift=RIGHT), run_time=0.6)
            self.wait(0.5)
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 6: THE EPIPHANY
    # =========================================================================
    def scene_6_epiphany(self):
        """Key insight"""
        title = Text("💡 The Key Insight", font_size=36, color=HIGHLIGHT_YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        insight = VGroup(
            Text("Convert vertex capacity constraint", font_size=28),
            Text("into an EDGE capacity constraint!", font_size=28, color=SUCCESS_GREEN),
        ).arrange(DOWN, buff=0.4)
        insight.move_to(ORIGIN + UP * 0.5)
        
        for line in insight:
            self.play(FadeIn(line), run_time=0.8)
            self.wait(0.8)
        self.wait(1.5)
        self.play(FadeOut(insight))

        technique_name = Text("Vertex Splitting Technique", font_size=32, color=ACTIVE_BLUE)
        technique_name.move_to(ORIGIN)
        self.play(Write(technique_name))
        self.wait(2)
        self.play(FadeOut(technique_name))

        steps = VGroup(
            Text("1. Split each vertex into TWO nodes", font_size=24),
            Text("2. Connect them with an edge", font_size=24),
            Text("3. Edge capacity = vertex capacity", font_size=24),
            Text("4. Run standard Max Flow algorithm", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.move_to(ORIGIN)
        
        for step in steps:
            self.play(FadeIn(step, shift=RIGHT), run_time=0.6)
            self.wait(0.7)
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 7: VERTEX SPLITTING TECHNIQUE
    # =========================================================================
    def scene_7_vertex_splitting_technique(self):
        """Show the transformation"""
        title = Text("Vertex Splitting Transformation", font_size=32, color=ACTIVE_BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1)

        # Original node
        original_label = Text("Original Node:", font_size=24, color=WHITE)
        original_label.to_edge(LEFT, buff=0.5).shift(UP * 1.5)
        self.play(Write(original_label))
        
        orig_node = Circle(radius=0.5, color=HIGHLIGHT_YELLOW, fill_opacity=0.3, stroke_width=3)
        orig_node.move_to(LEFT * 3)
        orig_label = Text("u\nCap = C", font_size=20, color=WHITE)
        orig_label.move_to(orig_node.get_center())
        
        self.play(Create(orig_node), Write(orig_label))
        self.wait(1.5)

        # Arrow showing transformation
        transform_arrow = Arrow(LEFT * 1.5, RIGHT * 0.5, color=SUCCESS_GREEN, stroke_width=5, buff=0)
        transform_text = Text("Split!", font_size=24, color=SUCCESS_GREEN)
        transform_text.next_to(transform_arrow, UP, buff=0.2)
        self.play(Create(transform_arrow), Write(transform_text))
        self.wait(1)

        # Split nodes
        split_label = Text("Split into TWO:", font_size=24, color=WHITE)
        split_label.to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
        self.play(Write(split_label))
        
        in_node = Circle(radius=0.45, color=VERTEX_IN, fill_opacity=0.3, stroke_width=3)
        in_node.move_to(RIGHT * 2 + UP * 0.8)
        in_label = Text("u_in", font_size=20, color=WHITE)
        in_label.move_to(in_node.get_center())
        
        out_node = Circle(radius=0.45, color=VERTEX_OUT, fill_opacity=0.3, stroke_width=3)
        out_node.move_to(RIGHT * 2 + DOWN * 0.8)
        out_label = Text("u_out", font_size=20, color=WHITE)
        out_label.move_to(out_node.get_center())
        
        self.play(Create(in_node), Create(out_node), Write(in_label), Write(out_label))
        self.wait(1)

        # Edge between them
        connector = Arrow(in_node.get_bottom(), out_node.get_top(), color=ERROR_RED, stroke_width=4, buff=0.1)
        cap_label = Text("Capacity = C", font_size=18, color=ERROR_RED)
        cap_label.next_to(connector, RIGHT, buff=0.2)
        self.play(Create(connector), Write(cap_label))
        self.wait(2)

        # Explanation
        exp = Text("All flow through u must pass this edge!", font_size=22, color=SUCCESS_GREEN)
        exp.to_edge(DOWN, buff=0.5)
        self.play(Write(exp))
        self.wait(2.5)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 8: TRANSFORMATION EXAMPLE
    # =========================================================================
    def scene_8_transformation_example(self):
        """Full transformation example"""
        title = Text("Full Graph Transformation", font_size=32, color=ACTIVE_BLUE)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Original graph on left
        orig_title = Text("Original", font_size=22, color=WHITE)
        orig_title.to_edge(LEFT, buff=0.5).shift(UP * 2.5)
        self.play(Write(orig_title))

        # Nodes: A, B (cap=5), C
        orig_positions = {
            "A": LEFT * 4.5 + UP * 0.5,
            "B": LEFT * 4.5 + DOWN * 1,
            "C": LEFT * 2.5 + DOWN * 1,
        }
        
        orig_nodes = VGroup()
        for name in ["A", "B", "C"]:
            if name == "B":
                color = HIGHLIGHT_YELLOW
                label_text = f"{name}\nCap=5"
            else:
                color = NODE_DEFAULT
                label_text = name
            circle = Circle(radius=0.35, color=color, fill_opacity=0.3, stroke_width=2)
            circle.move_to(orig_positions[name])
            label = Text(label_text, font_size=16, color=WHITE)
            label.move_to(orig_positions[name])
            orig_nodes.add(VGroup(circle, label))
        
        self.play(Create(orig_nodes), run_time=1)
        
        # Edges: A->B (10), B->C (10)
        orig_edges = VGroup()
        edge1 = Arrow(orig_positions["A"] + DOWN * 0.35, orig_positions["B"] + UP * 0.35, 
                      color=EDGE_DEFAULT, stroke_width=2, buff=0)
        e1_label = Text("10", font_size=14, color=HIGHLIGHT_YELLOW).next_to(edge1, LEFT, buff=0.1)
        edge2 = Arrow(orig_positions["B"] + RIGHT * 0.35, orig_positions["C"] + LEFT * 0.35, 
                      color=EDGE_DEFAULT, stroke_width=2, buff=0)
        e2_label = Text("10", font_size=14, color=HIGHLIGHT_YELLOW).next_to(edge2, DOWN, buff=0.1)
        orig_edges.add(edge1, e1_label, edge2, e2_label)
        
        self.play(Create(orig_edges), run_time=1)
        self.wait(1.5)

        # Transformed graph on right
        trans_title = Text("Transformed", font_size=22, color=SUCCESS_GREEN)
        trans_title.to_edge(RIGHT, buff=0.5).shift(UP * 2.5)
        self.play(Write(trans_title))

        # Split nodes
        trans_positions = {
            "A_in": RIGHT * 2 + UP * 1.5,
            "A_out": RIGHT * 3 + UP * 1.5,
            "B_in": RIGHT * 2 + DOWN * 0.3,
            "B_out": RIGHT * 3 + DOWN * 0.3,
            "C_in": RIGHT * 2 + DOWN * 2,
            "C_out": RIGHT * 3 + DOWN * 2,
        }
        
        trans_nodes = VGroup()
        node_info = [
            ("A_in", VERTEX_IN), ("A_out", VERTEX_OUT),
            ("B_in", VERTEX_IN), ("B_out", VERTEX_OUT),
            ("C_in", VERTEX_IN), ("C_out", VERTEX_OUT),
        ]
        
        for name, color in node_info:
            circle = Circle(radius=0.3, color=color, fill_opacity=0.3, stroke_width=2)
            circle.move_to(trans_positions[name])
            label = Text(name.replace("_", "\n"), font_size=12, color=WHITE)
            label.move_to(trans_positions[name])
            trans_nodes.add(VGroup(circle, label))
        
        self.play(Create(trans_nodes), run_time=1.5)
        
        # Internal edges (vertex capacity)
        internal_edges = VGroup()
        for node_name in ["A", "B", "C"]:
            start = trans_positions[f"{node_name}_in"]
            end = trans_positions[f"{node_name}_out"]
            arrow = Arrow(start + RIGHT * 0.3, end + LEFT * 0.3, color=ERROR_RED, stroke_width=2, buff=0)
            if node_name == "B":
                cap = "5"
                color = ERROR_RED
            else:
                cap = "∞"
                color = GRAY
            cap_label = Text(cap, font_size=12, color=color)
            cap_label.next_to(arrow, UP, buff=0.05)
            internal_edges.add(arrow, cap_label)
        
        self.play(Create(internal_edges), run_time=1)
        self.wait(1)

        # External edges (original edges)
        external_edges = VGroup()
        # A_out -> B_in (10)
        e1 = Arrow(trans_positions["A_out"] + DOWN * 0.3, trans_positions["B_in"] + UP * 0.3,
                   color=EDGE_DEFAULT, stroke_width=2, buff=0)
        e1_label = Text("10", font_size=12, color=HIGHLIGHT_YELLOW).next_to(e1, LEFT, buff=0.1)
        # B_out -> C_in (10)
        e2 = Arrow(trans_positions["B_out"] + DOWN * 0.3, trans_positions["C_in"] + UP * 0.3,
                   color=EDGE_DEFAULT, stroke_width=2, buff=0)
        e2_label = Text("10", font_size=12, color=HIGHLIGHT_YELLOW).next_to(e2, RIGHT, buff=0.1)
        external_edges.add(e1, e1_label, e2, e2_label)
        
        self.play(Create(external_edges), run_time=1)
        self.wait(2)

        # Explanation
        exp = Text("Bottleneck is now the B_in → B_out edge (cap=5)", font_size=20, color=SUCCESS_GREEN)
        exp.to_edge(DOWN, buff=0.3)
        self.play(Write(exp))
        self.wait(2.5)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 9: DRY RUN INPUT
    # =========================================================================
    def scene_9_dry_run_input(self):
        """Show the example input"""
        title = Text("Dry Run: Example Input", font_size=36, color=HIGHLIGHT_YELLOW)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1)

        # Input display
        input_box = VGroup(
            Text("n=4, m=3, s=0, t=3", font_size=24, color=WHITE),
            Text("Vertex capacities: [-1, 3, 2, -1]", font_size=22, color=HIGHLIGHT_YELLOW),
            Text("Edges:", font_size=22, color=ACTIVE_BLUE),
            Text("  0 → 1 (cap=3)", font_size=20),
            Text("  1 → 2 (cap=2)", font_size=20),
            Text("  2 → 3 (cap=3)", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        input_box.move_to(ORIGIN + UP * 0.8)
        
        for item in input_box:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.5)
            self.wait(0.4)
        self.wait(1.5)

        # Original graph visualization
        positions = {
            0: LEFT * 3 + DOWN * 1,
            1: LEFT * 1 + DOWN * 1,
            2: RIGHT * 1 + DOWN * 1,
            3: RIGHT * 3 + DOWN * 1,
        }
        
        nodes = VGroup()
        for i in range(4):
            if i == 0 or i == 3:
                cap_text = f"{i}\n∞"
                color = NODE_DEFAULT
            elif i == 1:
                cap_text = f"{i}\nCap=3"
                color = HIGHLIGHT_YELLOW
            else:
                cap_text = f"{i}\nCap=2"
                color = HIGHLIGHT_YELLOW
            
            circle = Circle(radius=0.4, color=color, fill_opacity=0.3, stroke_width=3)
            circle.move_to(positions[i])
            label = Text(cap_text, font_size=18, color=WHITE)
            label.move_to(positions[i])
            nodes.add(VGroup(circle, label))
        
        self.play(Create(nodes), run_time=1.2)
        
        # Edges
        edges_data = [(0, 1, 3), (1, 2, 2), (2, 3, 3)]
        edges = VGroup()
        for u, v, cap in edges_data:
            arrow = Arrow(positions[u] + RIGHT * 0.4, positions[v] + LEFT * 0.4,
                         color=EDGE_DEFAULT, stroke_width=3, buff=0)
            label = Text(str(cap), font_size=18, color=HIGHLIGHT_YELLOW)
            label.next_to(arrow, UP, buff=0.1)
            edges.add(arrow, label)
        
        self.play(Create(edges), run_time=1)
        self.wait(2.5)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 10: DRY RUN SPLIT
    # =========================================================================
    def scene_10_dry_run_split(self):
        """Show the transformed graph"""
        title = Text("After Vertex Splitting", font_size=32, color=ACTIVE_BLUE)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(0.5)

        # Transformed graph with 8 nodes (2 per original node)
        # Layout: vertical pairs for each original node
        positions = {}
        for i in range(4):
            x_pos = -3 + i * 2
            positions[f"{i}_in"] = LEFT * x_pos + UP * 0.6
            positions[f"{i}_out"] = LEFT * x_pos + DOWN * 0.6
        
        # Create nodes
        nodes = VGroup()
        for i in range(4):
            # In node
            in_circle = Circle(radius=0.35, color=VERTEX_IN, fill_opacity=0.3, stroke_width=2)
            in_circle.move_to(positions[f"{i}_in"])
            in_label = Text(f"{i}_in", font_size=14, color=WHITE)
            in_label.move_to(positions[f"{i}_in"])
            nodes.add(VGroup(in_circle, in_label))
            
            # Out node
            out_circle = Circle(radius=0.35, color=VERTEX_OUT, fill_opacity=0.3, stroke_width=2)
            out_circle.move_to(positions[f"{i}_out"])
            out_label = Text(f"{i}_out", font_size=14, color=WHITE)
            out_label.move_to(positions[f"{i}_out"])
            nodes.add(VGroup(out_circle, out_label))
        
        self.play(Create(nodes), run_time=1.5)
        
        # Internal edges (vertex capacities)
        internal = VGroup()
        caps = ["∞", "3", "2", "∞"]
        for i, cap in enumerate(caps):
            arrow = Arrow(positions[f"{i}_in"] + DOWN * 0.35, 
                         positions[f"{i}_out"] + UP * 0.35,
                         color=ERROR_RED if cap != "∞" else GRAY, 
                         stroke_width=3, buff=0)
            label = Text(cap, font_size=16, color=ERROR_RED if cap != "∞" else GRAY)
            label.next_to(arrow, RIGHT, buff=0.15)
            internal.add(arrow, label)
        
        self.play(Create(internal), run_time=1)
        self.wait(1)

        # External edges (original edges: 0->1, 1->2, 2->3)
        external = VGroup()
        edge_info = [(0, 1, 3), (1, 2, 2), (2, 3, 3)]
        for u, v, cap in edge_info:
            arrow = Arrow(positions[f"{u}_out"] + RIGHT * 0.35,
                         positions[f"{v}_in"] + LEFT * 0.35,
                         color=EDGE_DEFAULT, stroke_width=3, buff=0)
            label = Text(str(cap), font_size=16, color=HIGHLIGHT_YELLOW)
            label.next_to(arrow, UP, buff=0.1)
            external.add(arrow, label)
        
        self.play(Create(external), run_time=1)
        self.wait(1.5)

        # Highlight the path
        path_text = Text("Path: 0_in → 0_out → 1_in → 1_out → 2_in → 2_out → 3_in → 3_out",
                        font_size=18, color=SUCCESS_GREEN)
        path_text.to_edge(DOWN, buff=0.8)
        self.play(Write(path_text))
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 11: MAX FLOW RESULT
    # =========================================================================
    def scene_11_max_flow_result(self):
        """Show the max flow result"""
        title = Text("Maximum Flow Result", font_size=36, color=SUCCESS_GREEN)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.5)

        # Bottleneck analysis
        analysis = VGroup(
            Text("Bottleneck Analysis:", font_size=28, color=ACTIVE_BLUE),
            Text("Path capacities:", font_size=24),
            Text("  0_in → 0_out: ∞", font_size=22, color=GRAY),
            Text("  0_out → 1_in: 3", font_size=22),
            Text("  1_in → 1_out: 3", font_size=22),
            Text("  1_out → 2_in: 2", font_size=22),
            Text("  2_in → 2_out: 2", font_size=22, color=ERROR_RED),
            Text("  2_out → 3_in: 3", font_size=22),
            Text("  3_in → 3_out: ∞", font_size=22, color=GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        analysis.move_to(ORIGIN + UP * 0.5)
        
        for item in analysis[:2]:
            self.play(FadeIn(item), run_time=0.5)
            self.wait(0.3)
        
        for item in analysis[2:]:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.4)
            self.wait(0.3)
        self.wait(1.5)

        # Bottleneck
        bottleneck = Text("Bottleneck: min(∞, 3, 3, 2, 2, 3, ∞) = 2", 
                         font_size=26, color=RESULT_TEAL)
        bottleneck.to_edge(DOWN, buff=1.2)
        self.play(Write(bottleneck))
        self.wait(1.5)

        # Final answer
        answer = Text("Maximum Flow = 2", font_size=36, color=SUCCESS_GREEN)
        answer.to_edge(DOWN, buff=0.4)
        self.play(Write(answer))
        self.wait(3)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 12: COMPLEXITY ANALYSIS
    # =========================================================================
    def scene_12_complexity(self):
        """Complexity"""
        title = Text("Complexity Analysis", font_size=36, color=ACTIVE_BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # Transformation complexity
        trans_box = VGroup(
            Text("Transformation:", font_size=28, color=SUCCESS_GREEN),
            Text("• Double nodes: 2N", font_size=22),
            Text("• Edges: M + N", font_size=22),
            Text("• Time: O(N + M)", font_size=24, color=HIGHLIGHT_YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        trans_box.move_to(LEFT * 3 + UP * 0.3)
        
        for item in trans_box:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.5)
            self.wait(0.4)
        self.wait(1)

        # Max flow complexity
        flow_box = VGroup(
            Text("Dinic's Algorithm:", font_size=28, color=SUCCESS_GREEN),
            Text("• Nodes: V' = 2N", font_size=22),
            Text("• Edges: E' = M + N", font_size=22),
            Text("• Time: O(V'² × E')", font_size=24, color=HIGHLIGHT_YELLOW),
            Text("  = O(N² × (M+N))", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        flow_box.move_to(RIGHT * 3 + UP * 0.3)
        
        for item in flow_box:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.5)
            self.wait(0.4)
        self.wait(1.5)

        # Space
        space = Text("Space: O(N + M)", font_size=26, color=RESULT_TEAL)
        space.to_edge(DOWN, buff=0.5)
        self.play(Write(space))
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 13: CONCLUSION
    # =========================================================================
    def scene_13_conclusion(self):
        """Summary"""
        title = Text("Summary", font_size=40, color=SUCCESS_GREEN)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        takeaways = VGroup(
            Text("✓ Vertex capacity limits flow through a node", font_size=22),
            Text("✓ Vertex Splitting: Split u into u_in and u_out", font_size=22),
            Text("✓ Edge u_in → u_out has capacity = vertex capacity", font_size=22),
            Text("✓ Reduces to standard Max Flow problem", font_size=22),
            Text("✓ Use Dinic's Algorithm: O(V² × E)", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        takeaways.next_to(title, DOWN, buff=0.8)
        
        for t in takeaways:
            self.play(FadeIn(t, shift=RIGHT), run_time=0.6)
            self.wait(0.8)
        self.wait(2)
        self.play(FadeOut(takeaways), FadeOut(title))

        thanks = Text("Thank you for watching!", font_size=40, color=RESULT_TEAL)
        thanks.move_to(ORIGIN)
        self.play(Write(thanks))
        self.wait(3)
        
        self.clear_screen()


# To run:
# manim -pql AGR-002-max-flow-vertex-capacity.py AGR002MaxFlowScene
# For high quality: manim -pqh AGR-002-max-flow-vertex-capacity.py AGR002MaxFlowScene
