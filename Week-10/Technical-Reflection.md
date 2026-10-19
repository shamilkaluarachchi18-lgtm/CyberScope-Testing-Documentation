# Final Technical Reflection

## What Worked
The strongest part of the Week 10 testing was the clear relationship between the Python results and the Wireshark evidence.

The Python validator detected the newly introduced TCP port 8080 as a meaningful change and classified the runtime as `POTENTIAL COMPROMISE`. Wireshark then confirmed that port 8080 was actively accepting connections and transferring HTTP traffic.

The hostname tampering test also worked as expected. Changing a stable identity attribute produced a different Device DNA and a compromise result.

The restoration test was particularly useful because the original trusted Device DNA returned once the trusted state was restored.

## Main Challenge
A major issue identified earlier in the project was false-positive behaviour caused by dynamic network values such as temporary UDP ports.

Treating every network change as equally important would make the detection process unreliable.

## How I Addressed It
The Week 9 logic separated stable network attributes from dynamic UDP behaviour. This meant temporary UDP changes could remain informational while a new stable TCP service could still contribute to a compromise decision.

Week 10 then validated the final testing process using stable, controlled changes.

## What I Learned
I learned that device integrity cannot be judged only by whether a value changes. The security meaning of the change matters.

I also learned that combining trusted baseline comparison, Device-DNA hashing, changed-attribute reporting, and packet-level analysis provides better context than relying on only one technique.

## What I Would Do Differently
If repeating the project, I would classify attributes as stable, semi-stable, and dynamic before creating the first baseline.

I would also design the final automated test dataset earlier so that each technical component could be evaluated using the same test identifiers, expected results, and evidence format from the beginning.
