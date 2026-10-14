---
id: ml-reglas
title: "Machine learning: when the data writes the rules"
seo_title: "Machine learning: data writes the rules"
date: 2026-10-11
accent: aqua
hero: iceberg
projects: [formacion, reciclaje]
teacher: Daniel Sáenz
tags: [machine-learning, fundamentals, data-science]
summary: What machine learning is, how a project is built from start to finish, and why training the model is only the tip of the iceberg.
linkedin: In my first Data Science class one idea stuck with me - in traditional programming you write the rules; in machine learning, the data writes them for you. I summarise how a project is built (a mountain with three stages), the three ways to create a model, why training it is only the tip of the iceberg, and the recycling project where I put it to the test.
---

My first Data Science and generative AI class answered a question that seems obvious until you try to explain it: what exactly is machine learning? These are my notes, rewritten with my own examples, and a separate project where I put it to the test.

## What it is and where it fits

Artificial Intelligence is the broad field: getting machines to do things we associate with intelligence. Machine learning (ML) is one of its branches: instead of telling the computer what to do step by step, you give it examples and let it discover the patterns on its own.

Data Science is the craft around it. It combines statistics, programming and knowledge of the problem to understand data, make predictions and take better decisions.

## The idea that stuck with me: the cookie recipe

My instructor, Daniel Sáenz, explained it with a cookie recipe, and it's the image that stuck with me most. Imagine you want to bake cookies:

- **Traditional programming:** you have the ingredients and you write the recipe yourself, that is, the rules. Follow the steps and cookies come out: the answers.
- **Machine learning:** you have the ingredients and also the finished cookies. The algorithm is the one that invents the recipe that gets you from one to the other. That recipe, learned from examples, is the model.

{{include:galletas}}

The difference is who writes the rules. In the first case, you. In the second, the data.

An everyday example in any company: the customer service inbox. Hundreds of emails arrive every day and they have to be split into complaints, enquiries, document requests and cancellations.

- **With rules:** you write "if the email contains *complaint*, it goes to the complaints team". It works until an angry customer writes without using that word, or mixes two topics in one message. Every exception means adding another rule by hand.
- **With ML:** you show it thousands of emails that agents have already sorted. The model learns which features tend to go with each category (the vocabulary, the tone, what is being asked) and adapts when you give it new examples.

Of course, those emails contain personal data, so they would have to be anonymised before training.

## Four uses that keep showing up

**Recommendation.** Picture a cinema chain. If I know a customer likes releases from a certain genre and usually goes on Fridays, I can tell them a film of that genre is coming this week, with free seats in the area they usually pick. I could even feature the actor they've watched most often. With their permission, of course: good personalization also means respecting privacy.

**Game strategy.** Some models adjust difficulty to each player's level so the challenge is demanding but never impossible. Sometimes the difference is a matter of millimetres.

**Classification.** Back to customer service: a model that reads each email and sends it to the right team, so nobody wastes time forwarding. A more serious example is models that help detect pneumonia in chest X-rays, deployed in clinical settings during the pandemic.

**Prediction.** [Google's Flood Hub](https://blog.google/outreach-initiatives/sustainability/flood-hub-ai-flood-forecasting-more-countries/) forecasts river floods up to seven days ahead by combining weather forecasts and satellite imagery. It started as a pilot in India in 2018 with about 48 hours of lead time. A week's notice gives people time to reach safety.

## How a project is built: the mountain to climb

Before you start climbing you need to know where you're going: what do I want to predict and what decision will I make with it? From there, the path has three stages and the model takes up only the middle one. This is my map, with what to watch at each stage:

{{include:montana}}

And now, the obstacles at each stage, told the way I'd explain them to myself.

### First stage: the data

Everything starts with data, and it almost never arrives ready. The first problem is that it's incomplete or inconsistent: gaps, duplicates, dates written three different ways. Next, there are few labelled examples, because someone has to add the correct answer by hand. And finally, it tends to be imbalanced: in customer service emails there will be far more enquiries than complaints, and the model may end up ignoring the rare cases.

The solution is to invest time in preprocessing. First, profile the data to understand what's there. Then clean it, keep only what adds value, transform it into a format the model understands, enrich it with extra information and, at the end, validate that the result makes sense. It's not the flashiest part, but everything else depends on it.

### Second stage: build and train

With the data ready it's time to train, and four classic problems appear.

The first is choosing the algorithm. There are many and none is best at everything, so the sensible approach is to try several, compare their results with metrics such as precision or recall, and consider what kind of problem it is: classifying, predicting a number or grouping.

The second is overfitting: the model learns the training examples so well that it fails on new ones. To avoid it you split the data into training, validation and test sets, apply techniques that limit the model's complexity (regularization) and, if possible, get more data.

The third is hyperparameters, the settings the model doesn't learn by itself. Trying them by hand takes forever, so the search is automated with techniques such as Grid Search or Random Search.

And the fourth is computing power: training large models needs a lot of machine. You solve it by renting specialised processors in the cloud and splitting the training into small batches.

### Third stage: deploy and maintain

When the model works on your laptop, the hard part begins. The first problem is integrating it with the systems that already exist, which speak other formats and technologies. The usual approach is to offer it as a service other applications can call, documenting clearly what goes in and what comes out.

The second is that performance degrades over time, because the world changes and new data no longer looks like the training data. The solution is to monitor precision and recall continuously, with automatic alerts, and retrain the model with recent data.

Two more are worth remembering: handling a large volume of requests without slowing down (with cloud services that scale on their own) and making sure the model doesn't treat certain groups unfairly, which is exactly the next topic.

## Model governance: what you can't forget

Beyond the technical problems, three pillars hold up a serious project.

**Traceability.** Keep a record of every step, from the data to the deployment, with tools such as MLflow. If the model starts to fail, it lets you go back and see what changed: the data? some setting? It also lets you explain why a decision was made.

**Fairness.** Check that the model doesn't treat certain groups worse or repeat the biases in the data. If the email model served people who write formally first and left those who make spelling mistakes until last, it would be unfair. It's measured with specific metrics, regular audits and, in critical cases, a person reviewing.

**Continuous monitoring.** Watch the model in production to detect when the data changes and it stops getting things right, known as *concept drift*. A movie recommender goes stale when tastes change.

## Training the model is only the tip of the iceberg

When I started I thought the job was mostly writing the model's code, and that's a small part. Around it you have to collect and verify the data, extract its features, manage configuration and computing resources, have analysis tools, build the infrastructure that serves the model and watch it once it's running.

{{include:iceberg}}

The idea comes from a well-known 2015 Google paper, [*Hidden Technical Debt in Machine Learning Systems*](https://proceedings.neurips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf), which warns that ML systems pile up maintenance costs over time. That's why research and production are different worlds: in research what matters most is the model's performance, while in production response speed, ever-changing data, fairness and being able to explain decisions weigh just as much.

## Three ways to build a model

Luckily you don't have to climb the whole mountain from scratch in every project. In class we saw three levels, from least to most work. The deeper into the iceberg you go, the more control you have and the more you have to maintain.

{{include:niveles}}

An API saves you almost everything under the water. An end-to-end project puts it all in your hands.

## Putting it into practice

To put it to the test I'm building a recycling classifier with Teachable Machine, the Custom AI level tool: a photo of an object and the answer to which bin it goes in. It has its own page, with the plan, the tests and the results: [Recycling classifier]({{project:reciclaje}}).

## A project I won't build (and what it teaches)

My first idea was a mushroom classifier: edible or poisonous. I've deliberately ruled it out as an application. A model trained on a handful of photos will make mistakes, and in this problem the mistakes don't cost the same. Calling a toxic mushroom "edible" can be fatal. Calling an edible one "toxic" only costs you a dinner.

That's why it matters to look at more than the overall accuracy percentage. Here the key metric would be *recall*: of all the toxic mushrooms, how many does the model manage to flag as toxic? Also, many poisonous mushrooms look very much like edible ones, and identifying them safely is a job for an expert, not a photo.

The lesson is about design: choosing the right metric and thinking about the context of use are part of building a model. When real risk is involved, the model assists a person; it doesn't decide for them. And just in case: never use a photo model to decide what to eat.

## What I take away

Machine learning isn't magic and it isn't reserved for experts. It's a different way of solving problems in which data quality and maintenance weigh more than the algorithm itself, and training the model is only the tip of the iceberg. You can follow how the classifier is going on [its project page]({{project:reciclaje}}).
