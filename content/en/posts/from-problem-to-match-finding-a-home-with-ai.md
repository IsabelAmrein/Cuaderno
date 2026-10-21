---
id: caso-buscar-casa
title: "From problem to match: how we would approach finding a home with AI"
seo_title: "From problem to match: finding a home with AI"
date: 2026-10-19
order: 3
accent: sand
projects: [master]
hero: casa
teacher: David Rey
tags: [use-case, innovation, value-proposition]
module: Business Data and AI Strategy
kind: caso
case: buscar-casa-ia
summary: A class case study: how to go from a real problem, finding a home, to a data and AI idea with value, a business model and metrics.
linkedin: My third Data Science and generative AI class was an AI use case workshop. We began with a real problem, finding a home, and turned it into an idea with value based on data - a conversational agent, a match percentage and a business model. I explain the three steps of the canvas and what I take away.
---

This class was different from the earlier ones: instead of listening, we had to build. It is part of the *Business Data and AI Strategy* module and it was an **AI use case workshop**, the innovation session of the module. This article tells the case from the problem to the value proposition. It is the practical side that goes with the theory: the case will keep growing with the next classes and I will link it to the theory that explains it.

## The case

The teacher gave us a realistic case: a company dedicated to finding homes, working as an estate agency. As a team, on a collaborative whiteboard, we had to identify the problem, weigh alternatives, propose a solution with a <span class="hl">value proposition based on data</span> and outline a plan: how we would do it and how we would measure success. We finished with a four-minute mini pitch per team.

We worked with an adapted version of the *Lean Canvas*, a canvas for organising a business idea. It is worked through in three steps, and I think it is a good way to organise any idea:

{{include:vista}}

## Step 1: understand the problem

We started from the journey of a person who wants to buy a home, from the idea to the signature: they think about buying, research the area, search portals, get in touch and book viewings, negotiate the price, sign the deposit contract, look for financing and complete the purchase at the notary and the bank. The teacher marked two stretches as the focus of the case: searching portals and getting in touch to book viewings.

{{include:recorrido}}

The material raised two points of view: the home seeker's and the agency's, which loses quality leads because it cannot answer every call and cannot tell who is really interested. We chose the first. Along the journey, the seeker asks things like where to search, how much they can spend or what the fair price is; the filters do not answer what they really want to know, the information is scattered across images and texts, and everything is a manual and reactive process, with negotiation and paperwork that demand a lot of dedication. On top of that, from what classmates told us, searching for a home can be exhausting: hours comparing and fighting other people for the same properties. On the canvas we summed it up in three lines: there is no single portal for listings and information, a lot of time is lost searching, and the user experience is poor.

And what do people do today? Search on individual portals. It is the alternative that exists, and it has clear costs: time is lost, properties show up repeated and you have to call one by one.

## Step 2: design the solution

Our idea was to create a centralised model that unifies the search. Something like those comparison sites that bring many companies together and give you the best price for a train ticket, but with homes from several portals.

The key piece is a <span class="hl">conversational agent</span>. Instead of filling in filters, the person talks to it, voice included, and tells it what they are looking for and how they live. That conversation is unstructured data: the agent turns it into variables, matches them against the catalogue of homes and returns a **match percentage** for each one, explaining why it fits: "I think this flat is for you because of this and this, and you will feel good about this other thing".

{{include:agente}}

The homes would arrive through API connections with the platforms or, if that were not possible, through a data extraction model (*scraping*).

We set four **key objectives**:

- Win the customer's trust.
- Modernise the search process.
- Offer a conversational model that gives alternatives by voice.
- Convince people that the homes offered are chosen to suit them.

## The teacher's uncomfortable question

Here came the challenge: why would the biggest company in the sector, which already has similar tools, want to hire us or send us its traffic? Our answer was to turn it around: we were not going to sell it to them. Since they dominate almost the whole market, we sided with the small ones: bringing them together on one platform where all of them could coexist and compete with more strength.

## Step 3: turn it into a business

### The value proposition

Save time and improve the search experience with a <span class="hl">unified hyper-personalisation with extra services</span>. There are three ideas:

- **Hyper-personalisation.** With the photos from the platforms we generate a realistic 3D render and stage it according to what the person has told us. If they are looking for a home to live in with children, a dog and their mother-in-law, the property adapts to those needs so they can imagine living there; if they are single and want to share with friends, the render shows another use. Seeing yourself in the home increases interest.
- **Unification.** We bring the listings together and give the match percentage. We also handle the contact: if someone sees a property through our app, we send a ready-made message to the platform, the agency or the private seller to request a viewing.
- **Extra services.** When someone is already decided and liked their render, we can offer a renovation company that gives a good price for the style of the home, legal and financial guidance (what it will really cost, what is worth knowing about deposits or mortgage insurance) and a link to mortgage brokers.

### Who it is for

Two audiences: people looking for a flat to buy, because the idea is for sales, and the small property portals that want to join forces to offer a shared service.

### Two challenges

We raised two hard questions. The first, **how to bring the supply together**: with agreements with platforms, brokers and advertising, a B2B model. The second, **how to make it profitable**. On one side, income from renovations, brokers and legal services; on the other, a subscription for people searching for a home. A search lasts about three or four months, until you buy, and many people subscribe to an AI assistant for a specific piece of work and then cancel. Here it would be the same: you pay while the search lasts and get the whole personalised service. With the portals, agreements would be based on the traffic we send them, on leads or on subscription; that was left to define.

### The high-level concept

In one line: a pact with the small portals and a multimodal AI agent that talks to the customer and brings all the information. Behind it there is a recommendation system, API connections with the portals, the user's compiled data, each portal's data and an AI model that learns from the searches that end well. On the whiteboard we noted one more idea: an assistant made of sub-agents, depending on the stage the buyer is at.

### How we would measure success

The teacher gave us three starting points of view: the person searching (search time, number of physical viewings and satisfaction), the agency (quality leads and closed deals) and the company (revenue and user base). We kept three metrics:

- **Customer traffic**, organic and paid: how we get people to enter the platform.
- **Conversion via API**: of the people we talk to and give matches to, how many we send to a platform and close an in-person viewing. Since we are connected by API, the portals tell us; that viewing is our conversion, and the purchase would be an extra.
- **Satisfaction**: a survey at the end of the conversation.

## The missing piece: starting from the data too

In the annexes of the presentation there was an idea I found useful for this case. Traditional product design starts from the person and their problem, which is exactly what we did. But there is another way in: start from the **data as an asset** and look for where it fits. It boils down to a few questions: what data do we have and how good is it, is it unique or would it give us a differentiating position, in which of our customer's processes could it be useful, and can it produce an experience different from today's. And an important warning: the process is not linear, you go back and forth between exploring, fitting, ideating, executing and evaluating. The source cited in the presentation is *The Design Thinking Playbook*.

Applying it to our case, the assets would be the conversations with the people searching, the platforms' catalogue and their photographs: with them we build the match and the render.

## What I take away

- **Problem first, technology second.** The idea only makes sense because the pain is real: the hours lost searching for a home.
- **A good question changes the approach.** "Why would the big one want to work with you?" made us go from competing with it to uniting the small ones.
- **You can start from the problem or from the data.** It pays to do both, because the path is not linear.
- **An AI idea is also a business idea.** Without income and metrics, it stays a prototype. And everything rests on data: from conversation to variables, from variables to match and from match to conversion.

The case continues in the next classes.
