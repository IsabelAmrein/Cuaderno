---
id: reciclaje
title: Recycling classifier
subtitle: Which bin does this go in? One photo and an answer
date: 2026-10-12
status: en-marcha
accent: moss
hero: bins
stack: [Teachable Machine, Custom AI, Images]
summary: A model that, from a photo, says which bin each object goes in. Designed as an educational game to learn how to recycle, built with a no-code tool.
linkedin: I'm building a recycling classifier - a photo of an object and the answer to which bin it goes in. I share the plan, how I train it and, above all, where it fails.
---

## What I want to solve

Almost every child has a phone or tablet at home, and pointing at an object and seeing the answer is a way to learn recycling through play. This project builds that model with a no-code tool, to understand how it is trained and where it fails.

## How I build it

1. **Define the classes.** In Spain, four: yellow bin (plastic packaging, cans and cartons), blue (paper and cardboard), green (glass) and general waste. Rules vary by municipality, so this is a starting point.
2. **Gather data.** About 50 photos per class using objects from my home, varying background, light and angle.
3. **Train and test** the model with new objects I haven't photographed before.
4. **Note where it fails and why.**

## What I want to check

- **How much it depends on the data.** If every photo has the same background, what is the model really learning?
- **Which cases confuse it.** A carton looks like cardboard, but it goes in the yellow bin.
- **Which mistakes cost more.** Putting something non-recyclable in the yellow bin can spoil the recycling of everything else, whereas leaving a recyclable package in general waste simply loses it. It's the design lesson from the machine learning entry, with much less risk.

## What I use

Teachable Machine, a free Google tool that trains image classification models in the browser, no coding needed. It corresponds to the *Custom AI* level in the machine learning entry.

## Results

I'll publish them here once the tests are done: how many photos I used per class, the accuracy per class, the cases that fail and what I learned.

> It's an educational tool meant to be used with an adult nearby. It doesn't replace each municipality's official guidance.
