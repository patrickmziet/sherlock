# sherlock
Eval that tests LLMs ability to determine the culprit in murder mysteries. 

# TODO
- [X] Make enter story function
- [X] Test openai model
- [X] Make plotting code
- [X] Add claude API
- [X] Write serializers
- [ ] Decide how to score the LLMs over many stories
- [ ] Improve API request answer format. Give an example. Add option to "Think step by step..."
- [ ] Make 20 more stories
- [ ] Add other models


# Mysteries

## Murder Mystery Difficulty Criteria

Prompt: 

Write a Sherlock Holmes murder mystery story where throughout the story you introduce various characters, and give details which observed by themselves do not give away who the culprit is. But rather, by the end of the story there is enough detail for Sherlock to deduce who the culprit is. Please note that the culprit can never be Sherlock or Dr Watson, and that only one person can be the culprit. Furthermore this must be a new mystery, i.e. it cannot come from previously written Sherlock Holmes fictions. 

In the final paragraph of the story Sherlock must reveal who the culprit is with the sentence "The culprit is none other than __", and only then give the reasoning behind his reasoning. At the end of the story make a python list of all the suspects.

The story must meet the following criteria (especially the length criteria - it simply must meet it): 

## Easy

1. **Story Length**: At least 750 words. This length requirement must be strictly followed.
2. **Limited Suspects**: 3-5 suspects with clear motives.
3. **Straightforward Timeline**: Events occur in a linear, easy-to-follow sequence.
4. **Obvious Clues**: Clear and direct evidence pointing to the culprit.
5. **Simple Motive**: Easy-to-understand reason for the crime (e.g., jealousy, money).
6. **Single Crime Scene**: All relevant events occur in one location.
7. **No Red Herrings**: All clues are relevant to solving the mystery.
8. **Clear Alibis**: Most suspects have verifiable alibis, narrowing down the possibilities.
9. **Minimal Background**: Limited character backstories and history to consider.

Again, ensure that the story is at least 750 words.

## Medium

1. **Story Length**: At least 1500 words. This length requirement must be strictly followed.
2. **Moderate Number of Suspects**: 6-9 suspects with intertwining relationships.
3. **Slightly Complex Timeline**: Some events may overlap or have unclear ordering.
4. **Mix of Obvious and Subtle Clues**: Some evidence is clear, while other clues require more interpretation.
5. **Multifaceted Motive**: The reason for the crime involves multiple factors or is not immediately apparent.
6. **Multiple Crime Scenes**: Relevant events occur in 2-3 different locations.
7. **Some Red Herrings**: A few misleading clues that require elimination.
8. **Questionable Alibis**: Some suspects have alibis that are difficult to verify or have small inconsistencies.
9. **Moderate Backstory**: Character histories play a role in understanding motives and relationships.
10. **Secondary Crimes**: Minor related crimes or secrets that complicate the main investigation.
11. **Basic Forensic Evidence**: Introduction of simple forensic concepts.

Again, ensure that the story is at least 1500 words.

## Hard

1. **Story Length**: At least 3000 words. This length requirement must be strictly followed.
2. **Large Cast of Suspects**: 10-15 suspects with complex interconnected relationships.
3. **Complex Timeline**: Non-linear events, flashbacks, or unreliable narrator elements.
4. **Predominantly Subtle Clues**: Most evidence requires careful analysis and interpretation.
5. **Obscure or Twisted Motive**: The reason for the crime is highly complex, psychological, or initially seems absent.
6. **Multiple Interrelated Crime Scenes**: 4+ locations with important clues scattered across them.
7. **Numerous Red Herrings**: Many misleading clues that require careful elimination and analysis.
8. **Conflicting Alibis**: Suspects' stories contradict each other, creating a complex web of truths and lies.
9. **Extensive Backstories**: Deep character histories crucial to understanding the crime and motives.
10. **Advanced Forensic Evidence**: Incorporation of complex forensic techniques or cutting-edge technology.
11. **Psychological Elements**: Deep dive into characters' psyches, potentially including unreliable narrators or memory issues.
12. **Plot Twists**: Major revelations that force re-evaluation of previously established "facts."
13. **Sophisticated Cover-up**: Elaborate attempts to hide the truth, potentially involving multiple parties.

Again, ensure that the story is at least 3000 words.