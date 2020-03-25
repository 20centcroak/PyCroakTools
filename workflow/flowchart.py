import networkx as nx
import matplotlib.pyplot as plt
from pycroaktools.workflow.workflow import Workflow
from pycroaktools.workflow.step import Step
 
class Flowchart():
    """
    The Flowchart class makes use of the networkx library to render a Workflow as a graph.
    """

    def __init__(self, workflow: Workflow):
        """
        Builds the object.
        ---
        Parameters:
        - workflow: Workflow object
        """
        self.title = workflow.name
        self.graph = nx.Graph()
        paths = workflow.getAllPaths()
        for path in paths:
            for i in range(1,len(path),1):
                self.graph.add_edge(self.getStepText(path[i-1]), self.getStepText(path[i]))

    def display(self):
        
        # posx = [nx.spectral_layout(self.graph), nx.fruchterman_reingold_layout(self.graph), nx.circular_layout(self.graph), nx.random_layout(self.graph),  nx.spring_layout(self.graph)]
        posx = [nx.fruchterman_reingold_layout(self.graph), nx.spring_layout(self.graph)]

        for pos in posx:
            nx.draw(self.graph, with_labels=True, node_size=1500, node_color="skyblue", pos=pos)
            plt.title(self.title)
            plt.show()

    def getStepText(self, step:Step):
        return step.details if step.details else str(step.id)
