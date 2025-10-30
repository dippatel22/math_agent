import chromadb

from sentence_transformers import SentenceTransformer

from typing import List, Dict


VECTOR_DB_PATH = "./chromadb_math_jee"

COLLECTION_NAME = "math_jee_collection"

EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'


def setup_and_populate_vectordb():

    """

    Initializes the ChromaDB client at the specified path and populates

    the target collection with example math/JEE content.

    """

    print(f"Connecting to ChromaDB at: {VECTOR_DB_PATH}")



    try:

        chroma_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

    except Exception as e:

        print(f" Failed to initialize Chroma client: {e}")

        return


    embed_function = chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(

        model_name=EMBEDDING_MODEL_NAME

    )


    collection = chroma_client.get_or_create_collection(

        name=COLLECTION_NAME,

        embedding_function=embed_function

    )

   

    print(f" Collection '{COLLECTION_NAME}' is ready.")


    documents = [

    "A function $f(x)$ is **differentiable** at a point $x=a$ if and only if its right-hand derivative and left-hand derivative exist and are equal at $x=a$. Differentiability implies continuity, but not vice versa.",
    "The **chain rule** for differentiation states that if $y = f(g(x))$, then $\frac{dy}{dx} = f'(g(x)) \cdot g'(x)$. This is crucial for composite functions.",
    "The **Mean Value Theorem (Lagrange's)** states that if a function $f$ is continuous on $[a, b]$ and differentiable on $(a, b)$, then there exists at least one $c \in (a, b)$ such that $f'(c) = \frac{f(b) - f(a)}{b - a}$.",
    "To find the **local maximum or minimum** of a function $f(x)$, first find the critical points where $f'(x) = 0$ or $f'(x)$ is undefined. Then use the second derivative test ($f''(x)$) to classify them.",
    "**L'Hôpital's Rule** can be used to evaluate limits of the form $\frac{0}{0}$ or $\frac{\infty}{\infty}$. It states that $\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}$, provided the latter limit exists.",
    
    "The **formula for integration by parts** is $\int u dv = uv - \int v du$. This technique is essential for integrating products of functions, like $\int x \cos(x) dx$.",
    "A **definite integral** $\int_a^b f(x) dx$ represents the signed area of the region bounded by the graph of $f(x)$, the x-axis, and the vertical lines $x=a$ and $x=b$.",
    "The **fundamental theorem of calculus** (Part 2) states that if $F'(x) = f(x)$, then $\int_a^b f(x) dx = F(b) - F(a)$.",
    "The **Wallis' integral formula** is a useful reduction formula for evaluating $\int_0^{\pi/2} \sin^n(x) dx$ or $\int_0^{\pi/2} \cos^n(x) dx$.",
    "To find the **area between two curves** $f(x)$ and $g(x)$ from $x=a$ to $x=b$, where $f(x) \ge g(x)$, the area is given by $\int_a^b (f(x) - g(x)) dx$. [Image of Area between two curves using integration]",

    "The **equation of a circle** with center $(h, k)$ and radius $r$ is $(x-h)^2 + (y-k)^2 = r^2$. A common JEE problem involves finding the locus of a point.",
    "The **distance between two parallel lines** $Ax + By + C_1 = 0$ and $Ax + By + C_2 = 0$ is given by the formula $d = \frac{|C_1 - C_2|}{\sqrt{A^2 + B^2}}$.",
    "The **eccentricity of an ellipse** defined by $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ (with $a>b$) is $e = \sqrt{1 - \frac{b^2}{a^2}}$. The foci are at $(\pm ae, 0)$.",
    "The **equation of a tangent to the parabola** $y^2 = 4ax$ at the point $(x_1, y_1)$ is $yy_1 = 2a(x + x_1)$.",
    "The **condition for three points to be collinear** is that the area of the triangle formed by them must be zero, or the slope between any two pairs of points must be equal.",

    "The **sum of the first $n$ natural numbers** (also known as a triangular number) is given by the formula $S_n = \frac{n(n+1)}{2}$.",
    "The **sum of an infinite Geometric Progression (GP)** with first term $a$ and common ratio $r$ (where $|r| < 1$) is $S_{\infty} = \frac{a}{1-r}$.",
    "The **Binomial Theorem** states that for any non-negative integer $n$, $(x+y)^n = \sum_{k=0}^n \binom{n}{k} x^{n-k} y^k$.",
    "The **number of permutations** of $n$ distinct objects taken $r$ at a time is $P(n, r) = \frac{n!}{(n-r)!}$.",
    "The **Cauchy-Schwarz Inequality** for real numbers states that for any sequences $a_1, \dots, a_n$ and $b_1, \dots, b_n$, $(\sum_{i=1}^n a_i b_i)^2 \le (\sum_{i=1}^n a_i^2) (\sum_{i=1}^n b_i^2)$.",

    "In **Complex Numbers**, $\mathbf{i}$ is the imaginary unit, defined as $i^2 = -1$. The polar form of $z = x+iy$ is $z = r(\cos \theta + i \sin \theta)$.",
    "The **De Moivre's Theorem** states that $(\cos \theta + i \sin \theta)^n = \cos(n\theta) + i \sin(n\theta)$. This is used for finding roots and powers of complex numbers.",
    "For a **quadratic equation** $ax^2 + bx + c = 0$, the sum of the roots is $-\frac{b}{a}$ and the product of the roots is $\frac{c}{a}$.",
    "The **nature of the roots** of a quadratic equation is determined by the discriminant $D = b^2 - 4ac$. If $D>0$, roots are real and distinct; if $D=0$, roots are real and equal.",
    
    "The **scalar triple product (or box product)** of three vectors $\mathbf{a}, \mathbf{b}, \mathbf{c}$ is $\mathbf{a} \cdot (\mathbf{b} \times \mathbf{c})$, which represents the volume of the parallelepiped formed by the three vectors. If the product is zero, the vectors are coplanar.",
    "The **vector product (or cross product)** $\mathbf{a} \times \mathbf{b}$ results in a vector perpendicular to both $\mathbf{a}$ and $\mathbf{b}$, and its magnitude is $|\mathbf{a}||\mathbf{b}| \sin \theta$.",
    "The **equation of a plane** in normal form is $\mathbf{r} \cdot \mathbf{n} = d$, where $\mathbf{n}$ is the unit normal vector to the plane and $d$ is the perpendicular distance from the origin.",
    "The **shortest distance between two skew lines** with vector equations $\mathbf{r}_1 = \mathbf{a}_1 + \lambda \mathbf{b}_1$ and $\mathbf{r}_2 = \mathbf{a}_2 + \mu \mathbf{b}_2$ is $d = \frac{|(\mathbf{a}_2 - \mathbf{a}_1) \cdot (\mathbf{b}_1 \times \mathbf{b}_2)|}{|\mathbf{b}_1 \times \mathbf{b}_2|}$.",

    "**Bayes' Theorem** is used to find the conditional probability of an event $A$ given that event $B$ has occurred: $P(A|B) = \frac{P(B|A) P(A)}{P(B)}$.",
    "The **probability mass function (PMF)** for a **Binomial Distribution** is $P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}$, where $n$ is the number of trials and $p$ is the probability of success in a single trial."
]


    ids = [f"doc_{i+1}" for i in range(len(documents))]


    if collection.count() < len(documents):


        print(f"Adding {len(documents)} documents to the collection...")

        collection.add(

            documents=documents,

            ids=ids

        )

        print(f" Documents added. Total documents in collection: {collection.count()}")

    else:

        print(f"Collection already contains {collection.count()} documents. Skipping population.")

       

    return chroma_client
