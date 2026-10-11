---
id: ml-reglas
title: "Machine learning: when the data writes the rules"
date: 2026-10-11
accent: aqua
tags: [machine-learning, fundamentals, data-science]
summary: What machine learning is, how it differs from programming with rules, and why the hard part isn't training a model but keeping it working.
linkedin: In my first Data Science class one idea stuck with me - in traditional programming you write the rules; in machine learning, the data writes them for you. I explain it with my own examples, the mini project I'm about to build, and why I will NOT build a mushroom classifier.
---

My first class of the master's answered a question that seems obvious until you try to explain it: what exactly is machine learning? These are my notes, rewritten with my own examples, plus a mini project I'm going to build to put it to the test.

## What it is and where it fits

Artificial Intelligence is the broad field: getting machines to do things we associate with intelligence. Machine learning (ML) is one of its branches: instead of telling the computer what to do step by step, you give it examples and let it discover the patterns on its own.

Data Science is the craft around it. It combines statistics, programming and knowledge of the problem to understand data, make predictions and take better decisions.

## The idea that stuck with me: flipping the diagram

In traditional programming you write the rules, the program applies them to the data and produces answers. In ML the flow is reversed: you provide the data and the correct answers, and the algorithm works out the rules. Those learned rules are what we call a model.

| | Inputs | Output |
|---|---|---|
| Traditional programming | Rules and data | Answers |
| Machine learning | Data and answers | Rules (the model) |

An example with junk email:

- **With rules:** you write "if the message contains *prize* and *urgent*, it's spam". It works until spammers change their wording and you have to rewrite the rules by hand.
- **With ML:** you show it thousands of emails someone has already marked as spam or not spam. The model finds which combinations of features tend to go with each label, and it adapts when you give it new examples.

## Four uses that keep showing up

**Recommendation.** Picture a cinema chain. If I know a customer likes releases from a certain genre and usually goes on Fridays, I can tell them a film of that genre is coming this week, with free seats in the area they usually pick. I could even feature the actor they've watched most often. With their permission, of course: good personalization also means respecting privacy.

**Game strategy.** Some models adjust difficulty to each player's level so the challenge is demanding but never impossible. Sometimes the difference is a matter of millimetres.

**Classification.** The spam filter is the classic example. A more serious one: models that help detect pneumonia in chest X-rays, deployed in clinical settings during the pandemic.

**Prediction.** [Google's Flood Hub](https://blog.google/outreach-initiatives/sustainability/flood-hub-ai-flood-forecasting-more-countries/) forecasts river floods up to seven days ahead by combining weather forecasts and satellite imagery. It started as a pilot in India in 2018 with about 48 hours of lead time. A week's notice gives people time to reach safety.

## How an ML project works, in five steps

1. **Define the problem:** what do I want to predict and what decision will I make with it?
2. **Label the data:** examples together with their correct answer.
3. **Train the model:** the algorithm looks for patterns.
4. **Predict:** use the model on data it hasn't seen.
5. **Monitor:** check that it keeps getting things right as the world changes.

## The hard part isn't the model

What surprised me most is that training the model is usually the lightest part of the project. The difficulty is all around it:

- **The data.** It arrives incomplete, unlabelled or imbalanced. A model can only be as good as the data it learns from.
- **The training.** The big risk is overfitting: the model memorises the examples and fails on new cases. You guard against it by splitting the data into training, validation and test sets.
- **The deployment.** Integrating the model into real systems and maintaining it. Models degrade over time because the data changes, so they need retraining.

Launching a model is the easy part. Keeping it useful is the real job.

## Mini project: an image classifier

[Teachable Machine](https://teachablemachine.withgoogle.com/) is a free Google tool that trains classification models in your browser, no coding needed. This is my plan:

1. Pick three objects from my desk (for example a mug, a notebook and a pair of headphones).
2. Take about 50 photos of each with the webcam, varying background, light and angle.
3. Train the model and test it with new photos I didn't use for training.
4. Note where it fails and why.

I want to see how much the result depends on the variety of the data: if every photo has the same background, what is the model really learning? Once it's built, I'll update this article with my results.

## A project I won't build (and what it teaches)

My first idea was a mushroom classifier: edible or poisonous. I've deliberately ruled it out as an application. A model trained on a handful of photos will make mistakes, and in this problem the mistakes don't cost the same. Calling a toxic mushroom "edible" can be fatal. Calling an edible one "toxic" only costs you a dinner.

That's why it matters to look at more than the overall accuracy percentage. Here the key metric would be *recall*: of all the toxic mushrooms, how many does the model manage to flag as toxic? Also, many poisonous mushrooms look very much like edible ones, and identifying them safely is a job for an expert, not a photo.

The lesson is about design: choosing the right metric and thinking about the context of use are part of building a model. When real risk is involved, the model assists a person; it doesn't decide for them. And just in case: never use a photo model to decide what to eat.

## What I take away

Machine learning isn't magic and it isn't reserved for experts. It's a different way of solving problems in which data quality and maintenance weigh more than the algorithm itself. In the next article I'll share how the classifier went.
