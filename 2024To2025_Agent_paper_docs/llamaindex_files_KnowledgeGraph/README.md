# Enabling LLM development through knowledge graph visualization
_Discover how to empower LLM development through effective knowledge graph visualization. Learn to leverage yFiles for intuitive, interactive diagrams that simplify debugging and optimization in AI applications._

Visualizing knowledge graphs for accurate and intuitive AI interactions
-----------------------------------------------------------------------

![](../assets/images/blog/create-llama/yllama-graphai.c774db6927.png)

Knowledge graphs play a pivotal role in AI-driven applications, particularly in large language model (LLM)-powered chatbots. These graphs organize vast datasets, making information retrieval faster and more precise, which is essential for creating effective, context-aware responses.

Data frameworks like [LlamaIndex](https://www.llamaindex.ai/) bridge the gap between LLMs and various data structures that store the relevant information, making it easier to build applications that use AI features, for example with the help of [CreateLlama](https://github.com/run-llama/create-llama).

To provide the necessary context to the LLM, the AI integration uses a Graph Retrieval-Augmented Generation (RAG) approach. However, managing and interacting with knowledge graphs pose significant challenges for developers. These graphs often involve complex relationships and intricate structures, making debugging and optimization difficult without clear visualization tools.

The challenge of working with knowledge graphs
----------------------------------------------

Developers building AI agents often struggle with knowledge graphs due to the complexity of data relationships, the challenge of debugging response paths for accuracy, and the need to optimize data flow for performance. Without effective visualization tools, these obstacles can lead to inefficiencies, making it harder to interpret, debug, and refine AI-driven insights.

### Graph visualization matters for AI developers

AI developers need tools that simplify the interaction with complex data structures. A robust visualization framework makes it easier to debug and optimize the performance of the graph, ensuring that the chatbot or AI application works effectively.

[![Visualize complex data structures by clustering related information](../assets/images/blog/graph-aggregation.36ed9719d7.png)](../assets/images/blog/graph-aggregation.36ed9719d7.png "Visualize complex data structures by clustering related information")Visualize complex data structures by clustering related information

Graphs allow developers to explore the reasoning behind responses, validate the accuracy and relevance of data, and streamline the entire development process. By providing clear visual insights, graphs help accelerate the creation of more reliable and efficient AI systems.

### Data-driven visualization and interactivity are key

Integrating visual graph outputs into LLM frameworks like LlamaIndex provides significant benefits. Developers gain clarity in data relationships by visually mapping nodes and edges, making the flow of information more intuitive. Debugging becomes simpler as active nodes and pathways are highlighted, allowing errors to be quickly identified. Optimization improves as inefficiencies can be spotted and refined in real time.

Moreover, interactive visualizations offer significant advantages over static images, especially when dealing with large and evolving graph structures. They enable developers to seamlessly navigate complex data, zoom in on key areas, and reveal additional details as needed by interacting with the graph. Real-time updates further enhance this experience by reflecting changes instantly, allowing developers to monitor data flow dynamically, identify bottlenecks as they occur, and fine-tune their AI systems with immediate feedback.

[![Data-driven knowledge graph visualization in CreateLlama](../assets/images/blog/createllama-integration.173ea0b882.png)](../assets/images/blog/createllama-integration.173ea0b882.png "Data-driven knowledge graph visualization in CreateLlama")Data-driven knowledge graph visualization in CreateLlama

### Challenges in visualizing complex and dynamic graphs

Visualizing large and complex knowledge graphs presents significant challenges, including navigating massive data sets, identifying meaningful clusters, and managing dynamic interactions. Developers often struggle with rendering large graphs, which can appear cluttered and confusing, making it difficult to identify key relationships or areas of interest.

[![Automatic layouts improve readability of complex graphs](../assets/images/blog/bundled-circular-layout.f24b33a36b.png)](../assets/images/blog/bundled-circular-layout.f24b33a36b.png "Automatic layouts improve readability of complex graphs")Automatic layouts improve readability of complex graphs

Exploring dynamic graphs adds complexity, as real-time updates, interactive features such as zooming and folding, and grouping of nodes for clarity require advanced tools. Solutions like yFiles address these issues by offering customizable layouts, clustering options, and dynamic visualization capabilities that ensure clarity, scalability, and real-time interaction for efficient exploration and debugging of complex data.

yFiles - The Network Visualization SDK
--------------------------------------

[yFiles](https://www.yfiles.com/) addresses the challenges of visualizing knowledge graphs. This powerful software development kit (SDK) enables the creation of interactive diagrams and the analysis of complex networks and data relationships. By seamlessly integrating yFiles with LLM frameworks like [LlamaIndex](https://www.llamaindex.ai/), developers can create tailored, interactive, data-driven graph visualizations.

yFiles offers a versatile API that addresses all requirements for effective knowledge graph visualization. For example, requirements like the following can be solved easily:

*   Highlight active nodes and relationships during queries
*   Dynamically expand to reveal deeper connections
*   Offer real-time updates as data flows through the system

With yFiles, visualizing and interacting with knowledge graphs becomes intuitive, significantly reducing debugging time and facilitating better optimization of AI agents.

yFiles’ extensive library of automatic layout algorithms enables seamless integration, making it effortless for developers to render complex knowledge graphs, highlight activated nodes during operations, and dynamically adjust graph layouts for improved clarity and exploration. For instance, integrating yFiles with LlamaIndex allows developers to visually track data queries in real-time, simplifying debugging and optimization. Leveraging these existing algorithms provides developers with deeper insights and enhances the efficiency of their AI systems.

Integration in CreateLlama step by step instructions
----------------------------------------------------

The [yfiles-graph-for-create-llama](https://github.com/yWorks/yfiles-graph-for-create-llama) project illustrates, how yFiles can be integrated in a [CreateLlama](https://github.com/run-llama/create-llama) created project.

The project consists of two main components: the chatbot frontend with a graph visualization component and the Python backend that resolves user queries.

*   Backend: Powered by Python, the backend accesses the knowledge graph stored in LlamaIndex to generate responses. When a user asks a question, the backend queries the graph, retrieves relevant nodes, and returns them to the frontend for visualization.
*   Frontend: Built with React, the frontend visualizes interactions between the user and the knowledge graph. As the chatbot generates responses, yFiles dynamically updates the graph, highlighting relevant nodes and expanding them to provide additional context. This real-time interaction ensures a smooth experience for both developers and end users.

The basic steps on how to integrate yFiles in this project are outlined here:

1.  Create a new project with CreateLlama.
    
    Use the [CreateLlama CLI](https://github.com/run-llama/create-llama) to create a new project with the options specified in its tutorial
    
    *   npx create-llama@latest
    
2.  Obtain a free yFiles evaluation package.
    
    To use yFiles, get a free evaluation package[here](https://my.yworks.com/signup?product=YFILES_HTML_EVAL).
    
3.  Create a designated area in CreateLlama's frontend application.
    
    The yFiles graph component only requires a container element where the graph should be visualized. For example in the CreateLlama frontend, create a new designated container element (see [page.tsx](https://github.com/yWorks/yfiles-graph-for-create-llama/blob/main/frontend/app/page.tsx)) that holds our element:
    
    ```
<div className="w-[70%] w-full ml-4 bg-white rounded-xl shadow-xl">
  <KnowledgeGraph />
</div>

```

    
4.  Create a yFiles GraphComponent.
    
    A yFiles GraphComponent can be easily integrated in any HTML5 supporting framework by providing a container element to the GraphComponent constructor. For example, in React, a useMemo in combination with a useLayoutEffect is a possible solution as demonstrated in [use-graph-component.ts](https://github.com/yWorks/yfiles-graph-for-create-llama/blob/main/frontend/app/components/graphcomponent/use-graph-component.ts):
    
    ```
// create the GraphComponent 
const graphComponent = useMemo(() => {
  // include the license
  License.value = yFilesLicense
  // initialize the GraphComponent
  const gc = new GraphComponent()
  // use out of the box interactivity
  gc.inputMode = new GraphViewerInputMode()
  return gc
}, [])
```

    
    ```
// append it in the DOM
useLayoutEffect(() => {
  const gcContainer = graphComponentContainer.current!
  graphComponent.div.style.width = '100%'
  graphComponent.div.style.height = '100%'
  gcContainer.appendChild(graphComponent.div)

  return () => {
    gcContainer.innerHTML = ''
  }
}, [graphComponentContainer, graphComponent])

```

    
5.  Provide structured node and edge data.
    
    In the Python backend, the knowledge graph provides access to node and edge lists that is all that is needed to create a graph visualization (see [getData.py](https://github.com/yWorks/yfiles-graph-for-create-llama/blob/main/backend/app/getData.py)):
    
    ```
def get_knowledge_graph_info(params=None):
  index = get_index()
  nodes = index.property_graph_store.graph.nodes
  edges = index.property_graph_store.graph.triplets
  return {'nodes': create_node_list(nodes), 'edges': create_edge_list(edges)}

```

    
6.  Request knowledge graph data in the frontend.
    
    The GraphComponent in the frontend requires structured node/edge data to create a graph. This can be requested from the backend:
    
    ```
const fetchKnowledgeGraph = async () => {        
  const response = await axios.get(`${backend}/api/knowledge_graph/knowledge-graph`);
  setKnowledgeGraph(response.data.graph_info);
}
```

    
    yFiles' GraphBuilder can be configured to the structure of the provided data and manages build and update of the graph, for details, see [use-graph-builder.ts](https://github.com/yWorks/yfiles-graph-for-create-llama/blob/main/frontend/app/components/graphcomponent/use-graph-builder.ts).
7.  Add more yFiles features as needed.
    
    yFiles' extensive [documentation](https://docs.yworks.com/yfileshtml/#/home/), [developer's guide](https://docs.yworks.com/yfileshtml/#/dguide/) and [source code demos](https://www.yfiles.com/demos) provide an easy way to add more sophisticated features as needed. Common features for a knowledge graph visualization are illustrated in [yfiles-graph-for-create-llama](https://github.com/yWorks/yfiles-graph-for-create-llama):
    
    *   Data-driven coloring of nodes and edges
    *   Showing more context information on selection or hover of a graph item
    *   Automatic circular arrangement of graph items
    *   Interactive exploring of the local neighborhood of nodes by double click
    
    For more details, see the source code of this [CreateLlama project](https://github.com/yWorks/yfiles-graph-for-create-llama/blob/main/frontend/app/components/graphcomponent/ReactGraphComponent.tsx) or the yFiles' [source code demos](https://www.yfiles.com/demos).
8.  Run the project.
    
    Run backend and frontend as described in the [CreateLlama](https://github.com/run-llama/create-llama) documentation.
    

For a detailed implementation, follow the instructions and source code in the designated GitHub repository which contains a runnable project: [yfiles-graph-for-create-llama](https://github.com/yWorks/yfiles-graph-for-create-llama)

![](../assets/images/blog/graph-editing-with-llm/github-cat.8d3482efd5.png)

Graph your way to chatbot brilliance
------------------------------------

While [LlamaIndex](https://www.llamaindex.ai/) pairs instantly with yFiles, it is not the only framework that benefits from this integration. Tools like [LangChain](https://www.langchain.com/), [Haystack](https://haystack.deepset.ai/), and [Weaviate](https://weaviate.io/) can also leverage yFiles' powerful visualization capabilities to present and explore knowledge graphs more effectively.

Using yFiles with these frameworks simplifies the visualization and interpretability of complex relationships and data structures. Whether you're managing knowledge graphs, navigating intricate data paths, or analyzing interconnected datasets, yFiles delivers clarity and insight in real-time.

Regardless of your chosen indexing or graph-based framework, yFiles equips your projects with the tools to make interconnected data both comprehensible and actionable.

Learning and resources
----------------------

### Educational support

*   [yFiles - the Network Visualization SDK](https://www.yfiles.com/)
*   [Detailed yFiles documentation and developer's guide for graph visualization.](https://www.yworks.com/products/yfiles/documentation)
*   [yFiles source code demos.](https://www.yfiles.com/demos)
*   [create-llama GitHub repository.](https://github.com/run-llama/create-llama)
*   [Explore the general yFiles + React example for integrating graph visualization with React.](https://github.com/yWorks/yfiles-react-integration-basic)

Conclusion
----------

### The value proposition: Elite Knowledge Retrieval with yFiles

yFiles is an excellent choice for LLM-based projects that rely on graph data structures. It offers flexible and intuitive tools for visualizing complex relationships, making it easier to interpret and analyze large datasets.

Refine your chatbot and LLM workflows by integrating yFiles. Enhance your ability to explore and present interconnected data clearly and effectively, empowering users with precise insights and impressive visualization capabilities.

yFiles transforms the way developers interact with knowledge graphs, making them more accessible and intuitive. For LLM frameworks like LlamaIndex, yFiles offers superior visualization capabilities, ensuring efficient debugging, optimization, and data exploration. By incorporating yFiles into your workflow, you will certainly drive results by fully harnessing the power of graphs, enabling the creation of smarter, more reliable AI-driven applications

![](../assets/images/blog/year-in-review-2021/social-media-grafik.612bf92010.svg)

### Never miss a thing: