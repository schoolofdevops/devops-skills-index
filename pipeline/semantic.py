import numpy as np
from fastembed import TextEmbedding

MODEL_NAME = "BAAI/bge-small-en-v1.5"

ROLE_PROTOTYPES = {
    "DevOps Engineer": [
        "DevOps engineer automating CI CD, infrastructure as code, deployments, cloud platforms and developer delivery workflows",
        "build and release engineer responsible for deployment automation, build pipelines, release systems and developer tooling",
    ],
    "Site Reliability Engineer": [
        "site reliability engineer operating production services, on call, SLOs, incident response, observability, capacity and automation",
        "production engineer improving reliability, availability, latency and scalability of distributed online services",
    ],
    "Platform Engineer": [
        "platform engineer building internal developer platforms, paved roads, Kubernetes platforms, self service infrastructure and developer experience",
        "developer productivity engineer creating engineering platforms, CI systems, cloud environments and deployment tooling",
    ],
    "Cloud / Infrastructure": [
        "cloud infrastructure engineer designing and operating AWS Azure GCP, Kubernetes, Linux, networking and infrastructure automation",
        "systems infrastructure engineer running production compute, storage, networks, containers, configuration management and cloud operations",
    ],
    "DevSecOps": [
        "DevSecOps engineer securing CI CD pipelines, cloud infrastructure, containers, software supply chain, policy as code and platform security",
    ],
    "MLOps / AI Platform": [
        "MLOps engineer operating machine learning lifecycle, model training platforms, model registry, deployment, monitoring and production inference",
        "AI platform engineer building GPU infrastructure, model serving, LLM gateways, evaluation, observability and reliable AI production systems",
    ],
}

NEGATIVE_PROTOTYPES = [
    "customer success account management sales support onboarding renewals and customer relationships",
    "research scientist conducting scientific experiments, publishing research and developing novel machine learning algorithms without production operations ownership",
    "application software developer building product features, user interfaces, mobile applications or business logic without infrastructure ownership",
    "data analyst business analyst marketing finance human resources legal recruiting and administrative work",
    "solutions consultant pre sales sales engineer product demonstration and customer enablement",
]

class SemanticRoleMatcher:
    def __init__(self):
        self.model = TextEmbedding(model_name=MODEL_NAME)
        self.family_names=[]; texts=[]
        for family, examples in ROLE_PROTOTYPES.items():
            for example in examples: self.family_names.append(family); texts.append(example)
        self.positive=self._matrix(texts)
        self.negative=self._matrix(NEGATIVE_PROTOTYPES)

    def _matrix(self, texts):
        matrix=np.asarray(list(self.model.embed(texts)),dtype=np.float32)
        norms=np.linalg.norm(matrix,axis=1,keepdims=True); return matrix/np.maximum(norms,1e-9)

    def match_batch(self, documents):
        vectors=self._matrix(documents)
        pos=vectors@self.positive.T; neg=vectors@self.negative.T
        results=[]
        for i in range(len(documents)):
            best=int(np.argmax(pos[i])); positive=float(pos[i,best]); negative=float(np.max(neg[i])); margin=positive-negative
            results.append({"family":self.family_names[best],"semantic_score":round(positive,4),"negative_score":round(negative,4),"semantic_margin":round(margin,4)})
        return results
