"""
Manim Animation Script: AGR-001 - Minimum Cut on Small Graph
Production-quality, Zero-Overlap animation following Universal Manim DSA Prompt v2.0

Topic: Advanced Graphs - Stoer-Wagner Algorithm for Global Minimum Cut

Run command: manim -pql AGR-001-min-cut-small-graph.py AGR001MinCutScene
For high quality: manim -pqh AGR-001-min-cut-small-graph.py AGR001MinCutScene
"""

from manim import *
import numpy as np

# Color Palette (Following Universal Guidelines)
SUCCESS_GREEN = GREEN
ERROR_RED = RED
ACTIVE_BLUE = BLUE
HIGHLIGHT_YELLOW = YELLOW
RESULT_TEAL = TEAL
NODE_DEFAULT = WHITE
EDGE_DEFAULT = GRAY
MERGED_COLOR = ORANGE


class AGR001MinCutScene(Scene):
    """
    Complete animation for Minimum Cut on Small Graph problem.
    Follows Strict Sequential Flow - Zero Overlap Design Philosophy.
    """

    def construct(self):
        """Main animation orchestrator"""
        self.scene_1_intro()
        self.scene_2_problem()
        self.scene_3_real_world_analogy()
        self.scene_4_naive_approach()
        self.scene_5_epiphany()
        self.scene_6_algorithm_overview()
        self.scene_7_input_graph()
        self.scene_8_phase1()
        self.scene_9_phase2()
        self.scene_10_phase3()
        self.scene_11_final_result()
        self.scene_12_complexity()
        self.scene_13_conclusion()

    def clear_screen(self):
        """Helper to clear all mobjects with standard transition"""
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(0.3)

    # =========================================================================
    # SCENE 1: INTRO
    # =========================================================================
    def scene_1_intro(self):
        """High-level introduction"""
        # Main title
        title = Text("AGR-001: Minimum Cut on Small Graph", font_size=40, color=ACTIVE_BLUE)
        title.move_to(ORIGIN)
        self.play(Write(title), run_time=2)
        self.wait(2.5)
        self.play(FadeOut(title))

        # Topic
        topic = Text("Advanced Graph Algorithm", font_size=36, color=HIGHLIGHT_YELLOW)
        topic.move_to(ORIGIN)
        self.play(FadeIn(topic))
        self.wait(2)
        self.play(FadeOut(topic))

        # Algorithm name
        algo = Text("Stoer-Wagner Algorithm", font_size=42, color=SUCCESS_GREEN)
        algo.move_to(ORIGIN)
        self.play(Write(algo))
        self.wait(2.5)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 2: PROBLEM STATEMENT
    # =========================================================================
    def scene_2_problem(self):
        """Given vs Goal - Sequential display"""
        # GIVEN
        given_title = Text("GIVEN:", font_size=36, color=ACTIVE_BLUE)
        given_title.move_to(UP * 2)
        self.play(Write(given_title))
        self.wait(0.5)

        given_items = VGroup(
            Text("• Undirected weighted graph with n nodes", font_size=28),
            Text("• m edges, each with a positive weight", font_size=28),
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
            Text("• Find the GLOBAL minimum cut value", font_size=28),
            Text("• Partition nodes into 2 non-empty sets", font_size=28),
            Text("• Minimize total weight of crossing edges", font_size=28),
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
        """Power grid analogy"""
        # Title
        title = Text("Real-World Analogy: Power Grid", font_size=32, color=HIGHLIGHT_YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1.5)
        self.play(FadeOut(title))

        # Create power grid - matches our example graph
        # Nodes: 0, 1, 2, 3  Edges: (0,1,1), (1,2,2), (2,3,1), (0,3,2)
        positions = {
            0: LEFT * 2.5 + UP * 1.2,
            1: RIGHT * 2.5 + UP * 1.2,
            2: RIGHT * 2.5 + DOWN * 1.2,
            3: LEFT * 2.5 + DOWN * 1.2,
        }
        labels = ["Station 0", "Station 1", "Station 2", "Station 3"]
        
        stations = VGroup()
        for i in range(4):
            circle = Circle(radius=0.5, color=ACTIVE_BLUE, fill_opacity=0.3)
            circle.move_to(positions[i])
            text = Text(labels[i], font_size=18, color=WHITE)
            text.move_to(positions[i])
            stations.add(VGroup(circle, text))
        
        self.play(Create(stations), run_time=1.5)
        self.wait(1)

        # Edges matching the problem
        edges_info = [(0, 1, "1"), (1, 2, "2"), (2, 3, "1"), (0, 3, "2")]
        edges = VGroup()
        edge_labels = VGroup()
        
        for u, v, w in edges_info:
            start = positions[u]
            end = positions[v]
            line = Line(start, end, color=GRAY, stroke_width=3)
            edges.add(line)
            
            mid = (start + end) / 2
            direction = end - start
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.35
            label = Text(w, font_size=20, color=HIGHLIGHT_YELLOW)
            label.move_to(mid + perp)
            edge_labels.add(label)
        
        self.play(Create(edges), run_time=1)
        self.play(FadeIn(edge_labels), run_time=0.8)
        self.wait(1.5)

        # Explanation
        exp = Text("Find minimum-cost lines to cut that split the grid", font_size=24, color=WHITE)
        exp.to_edge(DOWN, buff=0.6)
        self.play(Write(exp))
        self.wait(2.5)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 4: NAIVE APPROACH
    # =========================================================================
    def scene_4_naive_approach(self):
        """Naive approach explanation"""
        title = Text("Naive Approach", font_size=36, color=ERROR_RED)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # Method description
        method = VGroup(
            Text("For each pair of nodes (s, t):", font_size=26),
            Text("   Run Max-Flow / Min-Cut algorithm", font_size=24),
            Text("   Track the minimum cut found", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        method.move_to(ORIGIN + UP * 0.5)
        
        for item in method:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.6)
            self.wait(0.6)
        self.wait(1.5)
        self.play(FadeOut(method))

        # Complexity warning
        warning = VGroup(
            Text("⚠️ Time Complexity:", font_size=28, color=ERROR_RED),
            Text("O(N² × MaxFlow) ≈ O(N² × V² × E)", font_size=26),
            Text("For N=200: TOO SLOW!", font_size=28, color=ERROR_RED),
        ).arrange(DOWN, buff=0.4)
        warning.move_to(ORIGIN)
        
        self.play(FadeIn(warning[0]))
        self.wait(0.8)
        self.play(FadeIn(warning[1]))
        self.wait(0.8)
        self.play(FadeIn(warning[2]))
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 5: THE EPIPHANY
    # =========================================================================
    def scene_5_epiphany(self):
        """Key insight"""
        title = Text("💡 The Key Insight", font_size=36, color=HIGHLIGHT_YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # Insight
        insight = VGroup(
            Text("We don't need to try all (s,t) pairs!", font_size=28),
            Text("Stoer-Wagner finds global min-cut", font_size=28),
            Text("by cleverly merging nodes.", font_size=28),
        ).arrange(DOWN, buff=0.4)
        insight.move_to(ORIGIN + UP * 0.5)
        
        for line in insight:
            self.play(FadeIn(line), run_time=0.8)
            self.wait(0.8)
        self.wait(1.5)
        self.play(FadeOut(insight))

        # Core idea
        core = VGroup(
            Text("Core Idea:", font_size=30, color=SUCCESS_GREEN),
            Text("1. Grow a set greedily (like Prim's MST)", font_size=24),
            Text("2. Last node's weight = candidate cut", font_size=24),
            Text("3. Merge last two nodes into one", font_size=24),
            Text("4. Repeat until 1 node remains", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        core.move_to(ORIGIN)
        
        self.play(FadeIn(core[0]))
        self.wait(0.5)
        for item in core[1:]:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.6)
            self.wait(0.7)
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 6: ALGORITHM OVERVIEW
    # =========================================================================
    def scene_6_algorithm_overview(self):
        """Stoer-Wagner algorithm steps"""
        title = Text("Stoer-Wagner Algorithm", font_size=36, color=ACTIVE_BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # MinimumCutPhase explanation
        phase_title = Text("MinimumCutPhase:", font_size=28, color=HIGHLIGHT_YELLOW)
        phase_title.next_to(title, DOWN, buff=0.6)
        self.play(Write(phase_title))
        self.wait(0.5)

        phase_steps = VGroup(
            Text("• Start with arbitrary node in set A", font_size=22),
            Text("• Repeat: Add most tightly connected node", font_size=22),
            Text("• 'Tightly connected' = max sum of edge weights to A", font_size=22),
            Text("• Last node added = cut candidate", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        phase_steps.next_to(phase_title, DOWN, buff=0.4)
        
        for step in phase_steps:
            self.play(FadeIn(step, shift=RIGHT), run_time=0.5)
            self.wait(0.5)
        self.wait(1.5)
        self.play(FadeOut(phase_title), FadeOut(phase_steps))

        # Main algorithm
        main_title = Text("Main Algorithm:", font_size=28, color=HIGHLIGHT_YELLOW)
        main_title.next_to(title, DOWN, buff=0.6)
        self.play(Write(main_title))
        self.wait(0.5)

        main_steps = VGroup(
            Text("1. min_cut = ∞", font_size=22),
            Text("2. While nodes > 1:", font_size=22),
            Text("     Run MinimumCutPhase → get (s, t, cut_value)", font_size=20),
            Text("     min_cut = min(min_cut, cut_value)", font_size=20),
            Text("     Merge t into s", font_size=20),
            Text("3. Return min_cut", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        main_steps.next_to(main_title, DOWN, buff=0.4)
        
        for step in main_steps:
            self.play(FadeIn(step, shift=RIGHT), run_time=0.4)
            self.wait(0.4)
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 7: INPUT GRAPH
    # =========================================================================
    def scene_7_input_graph(self):
        """Display the input graph"""
        title = Text("Step-by-Step Dry Run", font_size=36, color=HIGHLIGHT_YELLOW)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Input info
        input_title = Text("Input Graph", font_size=32, color=ACTIVE_BLUE)
        input_title.to_edge(UP, buff=0.4)
        self.play(Write(input_title))

        # Graph visualization
        positions = {
            0: LEFT * 2 + UP * 1,
            1: RIGHT * 2 + UP * 1,
            2: RIGHT * 2 + DOWN * 1,
            3: LEFT * 2 + DOWN * 1,
        }
        
        # Create nodes
        nodes = VGroup()
        node_labels = VGroup()
        for i in range(4):
            circle = Circle(radius=0.45, color=NODE_DEFAULT, fill_opacity=0.2, stroke_width=3)
            circle.move_to(positions[i])
            label = Text(str(i), font_size=26, color=WHITE)
            label.move_to(positions[i])
            nodes.add(circle)
            node_labels.add(label)
        
        self.play(Create(nodes), run_time=1)
        self.play(Write(node_labels), run_time=0.8)

        # Create edges: (0,1,1), (1,2,2), (2,3,1), (0,3,2)
        edges_data = [(0, 1, 1), (1, 2, 2), (2, 3, 1), (0, 3, 2)]
        edges = VGroup()
        weights = VGroup()
        
        for u, v, w in edges_data:
            line = Line(positions[u], positions[v], color=EDGE_DEFAULT, stroke_width=3)
            edges.add(line)
            
            mid = (positions[u] + positions[v]) / 2
            direction = positions[v] - positions[u]
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.35
            weight_label = Text(str(w), font_size=22, color=HIGHLIGHT_YELLOW)
            weight_label.move_to(mid + perp)
            weights.add(weight_label)
        
        self.play(Create(edges), run_time=1)
        self.play(FadeIn(weights), run_time=0.8)
        self.wait(1)

        # Input format text
        input_text = Text("n=4, m=4 | Edges: (0,1,1) (1,2,2) (2,3,1) (0,3,2)", font_size=20, color=WHITE)
        input_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(input_text))
        self.wait(2.5)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 8: PHASE 1 DRY RUN
    # =========================================================================
    def scene_8_phase1(self):
        """Phase 1 detailed walkthrough"""
        # Title
        title = Text("Phase 1", font_size=36, color=ACTIVE_BLUE)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Create graph on the left
        positions = {
            0: LEFT * 4 + UP * 1,
            1: LEFT * 1 + UP * 1,
            2: LEFT * 1 + DOWN * 1,
            3: LEFT * 4 + DOWN * 1,
        }
        
        nodes = VGroup()
        node_labels = VGroup()
        for i in range(4):
            circle = Circle(radius=0.4, color=NODE_DEFAULT, fill_opacity=0.2, stroke_width=3)
            circle.move_to(positions[i])
            label = Text(str(i), font_size=24, color=WHITE)
            label.move_to(positions[i])
            nodes.add(circle)
            node_labels.add(label)

        edges_data = [(0, 1, 1), (1, 2, 2), (2, 3, 1), (0, 3, 2)]
        edges = VGroup()
        edge_weights = VGroup()
        
        for u, v, w in edges_data:
            line = Line(positions[u], positions[v], color=EDGE_DEFAULT, stroke_width=3)
            edges.add(line)
            mid = (positions[u] + positions[v]) / 2
            direction = positions[v] - positions[u]
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.3
            wt = Text(str(w), font_size=18, color=HIGHLIGHT_YELLOW)
            wt.move_to(mid + perp)
            edge_weights.add(wt)

        graph = VGroup(edges, nodes, node_labels, edge_weights)
        self.play(Create(graph), run_time=1.2)
        self.wait(0.5)

        # Info panel on the right
        info_box = Rectangle(width=4, height=3.5, color=WHITE, stroke_width=1)
        info_box.to_edge(RIGHT, buff=0.5)
        info_box.shift(DOWN * 0.3)
        self.play(Create(info_box))

        # Step 1: Start with node 0
        step_label = Text("Step 1: Start with node 0", font_size=20, color=SUCCESS_GREEN)
        step_label.next_to(info_box, UP, buff=0.2)
        self.play(Write(step_label))
        
        # Highlight node 0
        self.play(nodes[0].animate.set_fill(SUCCESS_GREEN, opacity=0.6), run_time=0.5)
        
        # Show weights array
        weights_text = Text("weights = [-, 1, 0, 2]", font_size=18, color=WHITE)
        weights_text.move_to(info_box.get_center() + UP * 1)
        set_text = Text("Set A = {0}", font_size=18, color=ACTIVE_BLUE)
        set_text.move_to(info_box.get_center() + UP * 0.4)
        self.play(Write(weights_text), Write(set_text))
        self.wait(1.5)

        # Step 2: Pick node 3 (max weight = 2)
        self.play(FadeOut(step_label))
        step_label = Text("Step 2: Pick node 3 (weight=2)", font_size=20, color=SUCCESS_GREEN)
        step_label.next_to(info_box, UP, buff=0.2)
        self.play(Write(step_label))
        
        # Arrow pointing to node 3
        arrow = Arrow(positions[3] + DOWN * 0.8, positions[3] + DOWN * 0.1, 
                      color=ERROR_RED, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        self.play(Create(arrow))
        self.play(nodes[3].animate.set_fill(SUCCESS_GREEN, opacity=0.6), run_time=0.5)
        
        # Update info
        self.play(FadeOut(weights_text), FadeOut(set_text))
        weights_text = Text("weights = [-, 1, 1, -]", font_size=18, color=WHITE)
        weights_text.move_to(info_box.get_center() + UP * 1)
        set_text = Text("Set A = {0, 3}", font_size=18, color=ACTIVE_BLUE)
        set_text.move_to(info_box.get_center() + UP * 0.4)
        note = Text("(node 2 gets +1 from edge 3-2)", font_size=14, color=GRAY)
        note.move_to(info_box.get_center() + DOWN * 0.2)
        self.play(Write(weights_text), Write(set_text), Write(note))
        self.play(FadeOut(arrow))
        self.wait(1.5)

        # Step 3: Pick node 1 (weight=1, tie with node 2)
        self.play(FadeOut(step_label), FadeOut(note))
        step_label = Text("Step 3: Pick node 1 (weight=1)", font_size=20, color=SUCCESS_GREEN)
        step_label.next_to(info_box, UP, buff=0.2)
        self.play(Write(step_label))
        
        arrow = Arrow(positions[1] + UP * 0.8, positions[1] + UP * 0.1, 
                      color=ERROR_RED, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        self.play(Create(arrow))
        self.play(nodes[1].animate.set_fill(SUCCESS_GREEN, opacity=0.6), run_time=0.5)
        
        # Update info
        self.play(FadeOut(weights_text), FadeOut(set_text))
        weights_text = Text("weights = [-, -, 3, -]", font_size=18, color=WHITE)
        weights_text.move_to(info_box.get_center() + UP * 1)
        set_text = Text("Set A = {0, 3, 1}", font_size=18, color=ACTIVE_BLUE)
        set_text.move_to(info_box.get_center() + UP * 0.4)
        note = Text("(node 2 gets +2 from edge 1-2)", font_size=14, color=GRAY)
        note.move_to(info_box.get_center() + DOWN * 0.2)
        self.play(Write(weights_text), Write(set_text), Write(note))
        self.play(FadeOut(arrow))
        self.wait(1.5)

        # Step 4: Pick node 2 LAST
        self.play(FadeOut(step_label), FadeOut(note))
        step_label = Text("Step 4: Pick node 2 LAST", font_size=20, color=ERROR_RED)
        step_label.next_to(info_box, UP, buff=0.2)
        self.play(Write(step_label))
        
        arrow = Arrow(positions[2] + DOWN * 0.8, positions[2] + DOWN * 0.1, 
                      color=ERROR_RED, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        self.play(Create(arrow))
        self.play(nodes[2].animate.set_fill(ERROR_RED, opacity=0.6), run_time=0.5)
        self.play(FadeOut(arrow))
        self.wait(1)

        # Show result
        self.play(FadeOut(weights_text), FadeOut(set_text), FadeOut(step_label))
        
        result = VGroup(
            Text("s = node 1, t = node 2", font_size=18, color=WHITE),
            Text("Phase Cut = 3", font_size=22, color=RESULT_TEAL),
            Text("min_cut = min(∞, 3) = 3", font_size=18, color=SUCCESS_GREEN),
            Text("Action: Merge 2 into 1", font_size=18, color=MERGED_COLOR),
        ).arrange(DOWN, buff=0.25)
        result.move_to(info_box.get_center())
        
        for r in result:
            self.play(FadeIn(r), run_time=0.5)
            self.wait(0.5)
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 9: PHASE 2 DRY RUN
    # =========================================================================
    def scene_9_phase2(self):
        """Phase 2 with merged node"""
        title = Text("Phase 2 (After Merging 2→1)", font_size=32, color=ACTIVE_BLUE)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Show merged graph: nodes 0, 1+2, 3
        # After merge: edges (0, 1+2, w=1), (1+2, 3, w=1), (0, 3, w=2)
        positions = {
            0: LEFT * 3.5 + UP * 0.5,
            "1+2": RIGHT * 0.5 + UP * 1,
            3: LEFT * 1 + DOWN * 1.5,
        }
        
        nodes = VGroup()
        node_labels = VGroup()
        
        # Node 0
        c0 = Circle(radius=0.4, color=NODE_DEFAULT, fill_opacity=0.2, stroke_width=3)
        c0.move_to(positions[0])
        l0 = Text("0", font_size=24, color=WHITE)
        l0.move_to(positions[0])
        nodes.add(c0)
        node_labels.add(l0)
        
        # Merged node 1+2
        c12 = Circle(radius=0.5, color=MERGED_COLOR, fill_opacity=0.3, stroke_width=3)
        c12.move_to(positions["1+2"])
        l12 = Text("1+2", font_size=20, color=WHITE)
        l12.move_to(positions["1+2"])
        nodes.add(c12)
        node_labels.add(l12)
        
        # Node 3
        c3 = Circle(radius=0.4, color=NODE_DEFAULT, fill_opacity=0.2, stroke_width=3)
        c3.move_to(positions[3])
        l3 = Text("3", font_size=24, color=WHITE)
        l3.move_to(positions[3])
        nodes.add(c3)
        node_labels.add(l3)

        # Edges after merge
        edges_info = [
            (positions[0], positions["1+2"], "1"),
            (positions["1+2"], positions[3], "1"),
            (positions[0], positions[3], "2"),
        ]
        edges = VGroup()
        edge_labels = VGroup()
        
        for start, end, w in edges_info:
            line = Line(start, end, color=EDGE_DEFAULT, stroke_width=3)
            edges.add(line)
            mid = (start + end) / 2
            direction = end - start
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.35
            wt = Text(w, font_size=20, color=HIGHLIGHT_YELLOW)
            wt.move_to(mid + perp)
            edge_labels.add(wt)

        graph = VGroup(edges, nodes, node_labels, edge_labels)
        graph.shift(LEFT * 0.5)
        self.play(Create(graph), run_time=1.2)

        # Info panel
        info_box = Rectangle(width=4.5, height=3, color=WHITE, stroke_width=1)
        info_box.to_edge(RIGHT, buff=0.3)
        info_box.shift(DOWN * 0.5)
        self.play(Create(info_box))

        # Step 1: Start with node 0
        step_label = Text("Start: node 0", font_size=20, color=SUCCESS_GREEN)
        step_label.next_to(info_box, UP, buff=0.2)
        self.play(Write(step_label))
        self.play(nodes[0].animate.set_fill(SUCCESS_GREEN, opacity=0.6), run_time=0.4)
        
        weights_text = Text("weights = [-, 1, 2]", font_size=18, color=WHITE)
        weights_text.move_to(info_box.get_center() + UP * 0.8)
        idx_text = Text("(indices: 1+2, 3)", font_size=14, color=GRAY)
        idx_text.move_to(info_box.get_center() + UP * 0.4)
        self.play(Write(weights_text), Write(idx_text))
        self.wait(1)

        # Step 2: Pick node 3 (weight=2)
        self.play(FadeOut(step_label))
        step_label = Text("Pick: node 3 (weight=2)", font_size=20, color=SUCCESS_GREEN)
        step_label.next_to(info_box, UP, buff=0.2)
        self.play(Write(step_label))
        self.play(nodes[2].animate.set_fill(SUCCESS_GREEN, opacity=0.6), run_time=0.4)
        
        self.play(FadeOut(weights_text), FadeOut(idx_text))
        weights_text = Text("weights = [-, 2, -]", font_size=18, color=WHITE)
        weights_text.move_to(info_box.get_center() + UP * 0.8)
        note = Text("(1+2 gets +1 from edge 3-(1+2))", font_size=14, color=GRAY)
        note.move_to(info_box.get_center() + UP * 0.3)
        self.play(Write(weights_text), Write(note))
        self.wait(1)

        # Step 3: Pick node 1+2 LAST
        self.play(FadeOut(step_label), FadeOut(note))
        step_label = Text("Pick: node 1+2 LAST", font_size=20, color=ERROR_RED)
        step_label.next_to(info_box, UP, buff=0.2)
        self.play(Write(step_label))
        self.play(nodes[1].animate.set_fill(ERROR_RED, opacity=0.6), run_time=0.4)
        self.wait(1)

        # Result
        self.play(FadeOut(weights_text), FadeOut(step_label))
        
        result = VGroup(
            Text("s = node 3, t = node 1+2", font_size=16, color=WHITE),
            Text("Phase Cut = 2", font_size=22, color=RESULT_TEAL),
            Text("min_cut = min(3, 2) = 2 ✓", font_size=18, color=SUCCESS_GREEN),
            Text("Action: Merge 1+2 into 3", font_size=16, color=MERGED_COLOR),
        ).arrange(DOWN, buff=0.2)
        result.move_to(info_box.get_center())
        
        for r in result:
            self.play(FadeIn(r), run_time=0.4)
            self.wait(0.4)
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 10: PHASE 3 DRY RUN
    # =========================================================================
    def scene_10_phase3(self):
        """Final phase with 2 nodes"""
        title = Text("Phase 3 (Final)", font_size=36, color=ACTIVE_BLUE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Only 2 nodes: 0 and merged super-node
        c0 = Circle(radius=0.5, color=NODE_DEFAULT, fill_opacity=0.2, stroke_width=3)
        c0.move_to(LEFT * 2.5)
        l0 = Text("0", font_size=28, color=WHITE)
        l0.move_to(LEFT * 2.5)
        
        c_super = Circle(radius=0.7, color=MERGED_COLOR, fill_opacity=0.3, stroke_width=3)
        c_super.move_to(RIGHT * 2.5)
        l_super = Text("3+1+2", font_size=22, color=WHITE)
        l_super.move_to(RIGHT * 2.5)
        
        edge = Line(LEFT * 2.5, RIGHT * 2.5, color=EDGE_DEFAULT, stroke_width=4)
        edge_weight = Text("3", font_size=24, color=HIGHLIGHT_YELLOW)
        edge_weight.next_to(edge, UP, buff=0.2)
        
        graph = VGroup(edge, c0, l0, c_super, l_super, edge_weight)
        self.play(Create(graph), run_time=1.5)
        self.wait(1)

        # Explanation
        exp1 = Text("Only 2 nodes remain → trivial phase", font_size=24, color=WHITE)
        exp1.to_edge(DOWN, buff=1.5)
        self.play(Write(exp1))
        self.wait(1)
        self.play(FadeOut(exp1))

        # Result
        result = VGroup(
            Text("Phase Cut = 3", font_size=26, color=RESULT_TEAL),
            Text("min_cut = min(2, 3) = 2", font_size=22, color=WHITE),
            Text("(no change)", font_size=20, color=GRAY),
        ).arrange(DOWN, buff=0.3)
        result.to_edge(DOWN, buff=0.8)
        
        for r in result:
            self.play(FadeIn(r), run_time=0.5)
            self.wait(0.5)
        self.wait(2)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 11: FINAL RESULT
    # =========================================================================
    def scene_11_final_result(self):
        """Show the final answer with visualization"""
        title = Text("Final Result", font_size=40, color=SUCCESS_GREEN)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.5)

        # Original graph with cut highlighted
        positions = {
            0: LEFT * 2.5 + UP * 1,
            1: RIGHT * 2.5 + UP * 1,
            2: RIGHT * 2.5 + DOWN * 1,
            3: LEFT * 2.5 + DOWN * 1,
        }
        
        # Nodes colored by partition
        nodes = VGroup()
        node_labels = VGroup()
        for i in range(4):
            if i in [0, 3]:
                color = ACTIVE_BLUE
            else:
                color = SUCCESS_GREEN
            circle = Circle(radius=0.45, color=color, fill_opacity=0.5, stroke_width=3)
            circle.move_to(positions[i])
            label = Text(str(i), font_size=26, color=WHITE)
            label.move_to(positions[i])
            nodes.add(circle)
            node_labels.add(label)

        # Edges - cut edges in red, others in gray
        # Cut edges: (0,1), (2,3)  Non-cut: (1,2), (0,3)
        edges_data = [
            (0, 1, 1, True),   # cut
            (1, 2, 2, False),  # not cut
            (2, 3, 1, True),   # cut
            (0, 3, 2, False),  # not cut
        ]
        edges = VGroup()
        edge_weights = VGroup()
        
        for u, v, w, is_cut in edges_data:
            color = ERROR_RED if is_cut else EDGE_DEFAULT
            width = 5 if is_cut else 3
            line = Line(positions[u], positions[v], color=color, stroke_width=width)
            edges.add(line)
            
            mid = (positions[u] + positions[v]) / 2
            direction = positions[v] - positions[u]
            perp = np.array([-direction[1], direction[0], 0])
            if np.linalg.norm(perp) > 0:
                perp = perp / np.linalg.norm(perp) * 0.35
            wt = Text(str(w), font_size=20, color=HIGHLIGHT_YELLOW)
            wt.move_to(mid + perp)
            edge_weights.add(wt)

        graph = VGroup(edges, nodes, node_labels, edge_weights)
        self.play(Create(graph), run_time=2)
        self.wait(1)

        # Partition labels at bottom
        set_a = Text("Set A: {0, 3}", font_size=22, color=ACTIVE_BLUE)
        set_a.to_corner(DL, buff=0.4)
        set_b = Text("Set B: {1, 2}", font_size=22, color=SUCCESS_GREEN)
        set_b.to_corner(DR, buff=0.4)
        self.play(Write(set_a), Write(set_b))
        self.wait(1)

        # Final answer - centered at bottom
        answer = VGroup(
            Text("Cut edges: (0,1) + (2,3) = 1 + 1", font_size=24, color=ERROR_RED),
            Text("Minimum Cut = 2", font_size=32, color=RESULT_TEAL),
        ).arrange(DOWN, buff=0.3)
        answer.next_to(graph, DOWN, buff=0.6)
        
        self.play(FadeIn(answer[0]))
        self.wait(0.5)
        self.play(FadeIn(answer[1]))
        self.wait(3)
        
        self.clear_screen()

    # =========================================================================
    # SCENE 12: COMPLEXITY ANALYSIS
    # =========================================================================
    def scene_12_complexity(self):
        """Time and Space complexity"""
        title = Text("Complexity Analysis", font_size=36, color=ACTIVE_BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # Time complexity
        time_box = VGroup(
            Text("Time Complexity", font_size=28, color=SUCCESS_GREEN),
            Text("• N-1 phases", font_size=22),
            Text("• Each phase: O(N²) scans", font_size=22),
            Text("• Total: O(N³)", font_size=26, color=HIGHLIGHT_YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        time_box.move_to(LEFT * 3 + DOWN * 0.3)
        
        for item in time_box:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.5)
            self.wait(0.4)
        self.wait(1)

        # Space complexity
        space_box = VGroup(
            Text("Space Complexity", font_size=28, color=SUCCESS_GREEN),
            Text("• Adjacency matrix: O(N²)", font_size=22),
            Text("• Auxiliary arrays: O(N)", font_size=22),
            Text("• Total: O(N²)", font_size=26, color=HIGHLIGHT_YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        space_box.move_to(RIGHT * 3 + DOWN * 0.3)
        
        for item in space_box:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.5)
            self.wait(0.4)
        self.wait(2.5)
        
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
            Text("✓ Global Min Cut partitions graph with min crossing weight", font_size=22),
            Text("✓ Stoer-Wagner: O(N³) deterministic algorithm", font_size=22),
            Text("✓ Works for undirected weighted graphs", font_size=22),
            Text("✓ Key: Greedily grow set, merge last two nodes", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        takeaways.next_to(title, DOWN, buff=0.8)
        
        for t in takeaways:
            self.play(FadeIn(t, shift=RIGHT), run_time=0.6)
            self.wait(0.8)
        self.wait(2)
        self.play(FadeOut(takeaways), FadeOut(title))

        # Thank you
        thanks = Text("Thank you for watching!", font_size=40, color=RESULT_TEAL)
        thanks.move_to(ORIGIN)
        self.play(Write(thanks))
        self.wait(3)
        
        self.clear_screen()


# To run:
# manim -pql AGR-001-min-cut-small-graph.py AGR001MinCutScene
# For high quality: manim -pqh AGR-001-min-cut-small-graph.py AGR001MinCutScene
