---
layout: default
title: Streaming Readout Plugins
order: 37
description: Configure streaming readout and implement worker payloads, crate processing, timing, and output
permalink: /documentation/sro/plugins/
---

# Streaming Readout Plugins

**Upcoming in the next release.** GEMC's `sro` factory routes contributions from all event workers to a
separate collector thread for each crate. A crate combines its channels into time frames and writes through
its own output sink. The experiment plugin defines the payload, electronics response, frame format, and
unfinished-frame policy. GEMC supplies the threads, bounded queues, ordering, and run lifecycle.

**SRO is off unless requested with %%format: sro%%.** Loading a detector plugin or setting %%eventTimeWidth%%
does not activate it. Ordinary CSV, ROOT, and HIPO selections continue to use their existing output paths.

Use [Digitization Plugins](/home/documentation/sensitivity/gplugins/) for detector hit processing and
[Output Plugins](/home/documentation/output/gplugin/) for event/run serialization. An SRO implementation uses
`GSROImplementationFactory`; it is selected by %%implementation%% under the generic %%sro%% format.

## On this page

- [Activate the example SRO](#activate-the-example-sro)
- [Event workers and crate threads](#event-workers-and-crate-threads)
- [Event time and frame completeness](#event-time-and-frame-completeness)
- [Define a streaming implementation](#define-a-streaming-implementation)
- [Required objects and callbacks](#required-objects-and-callbacks)
- [The callback lifecycle](#the-callback-lifecycle)
- [Required author decisions](#decisions-the-implementation-author-must-make)
- [Crate limits](#why-crate-limits-are-separate)
- [Simple random-ADC example](#simple-random-adc-example)
- [FT-Cal implementation](#ft-cal-implementation-and-current-scope)
- [Validation and remaining work](#validation-and-remaining-work)

## Activate the example SRO

Use GEMC's [random-ADC example](https://github.com/gemc/src/tree/main/examples/basic/sro). It sends a geantino
through four scoring planes and maps them to two crates. No experiment database is needed.

With the Geant4 build environment loaded, compile from the GEMC source repository:

```sh
meson compile -C build gemc example_sro
```

Generate the geometry and run in a scratch directory, using the paths from that same source checkout:

```sh
gemc_src="$PWD"
sro_run=$(mktemp -d /tmp/gemc-sro-example.XXXXXX)
cp "$gemc_src/examples/basic/sro/sro.yaml" "$sro_run/"
cd "$sro_run"
"$gemc_src/build/subprojects/pygemc/python_env/bin/python" \
  "$gemc_src/examples/basic/sro/sro.py" -f ascii
"$gemc_src/build/bin/gemc" sro.yaml \
  -plugin_path="$gemc_src/build/examples/basic/sro"
```

The supplied %%sro.yaml%% already requests SRO through these settings:

```yaml
eventTimeWidth: 10*ns
gstreamer:
  - format: sro
    filename: simple_sro
    implementation: example_sro
```

The card runs ten events on four workers and enables %%recordZeroEdep%% so the geantino produces hits.
The example writes %%simple_sro_r1_crate1.csv%% and %%simple_sro_r1_crate2.csv%%, combining contributions from
all workers. These are frame files produced by the example's sink; their CSV encoding does not select
GEMC's ordinary %%format: csv%% event streamer.

Relative basenames write in the working directory; an absolute %%filename%% selects another location.
Crates are created on first dispatch, so crates receiving no payload have no file. An active crate can have
only a CSV header if no complete frame is available. This example overwrites matching filenames; choose a
new basename to retain earlier output.

### Optional separate configuration card

For an existing detector card, save its SRO selection in a separate override if you want to switch outputs
without editing the normal card. For this example, save the settings above as %%sro_output.yaml%% and run:

```sh
"$gemc_src/build/bin/gemc" sro.yaml sro_output.yaml \
  -plugin_path="$gemc_src/build/examples/basic/sro"
```

The example's base card already enables SRO; the override is redundant here and illustrates the syntax.
Later YAML files override earlier ones; command-line options override YAML. With a normal base card that
has no %%sro%% entry, omitting the override keeps SRO disabled. A separate card is optional; output files
always belong to the implementation's crate sinks.

To request SRO and ordinary event output together, place both entries in the same %%gstreamer%% list:

```yaml
eventTimeWidth: 10*ns
gstreamer:
  - format: csv
    filename: example_events
  - format: sro
    filename: simple_sro
    implementation: example_sro
```

Ordinary event output still depends on what the detector digitizer provides. The toy digitizer supplies
SRO samples only; adding a CSV entry does not turn its ADC payload into ordinary digitized hit data.
For an experiment configuration, see [FT-Cal / JLAB Output](/home/documentation/output/jlabsro/).

### Required settings and available choices

| Setting | Requirement or choice |
|---|---|
| %%format%% | Must be %%sro%% to activate this mechanism. |
| %%filename%% | Required output basename; the implementation adds crate/run names and extensions. |
| %%implementation%% | Required library basename, %%example_sro%% for this example. |
| %%type%% | Optional; defaults to %%stream%% for SRO. Any other value is rejected. |
| %%eventTimeWidth%% | The example requires an explicit positive integral width in ns. |
| %%n%%, %%nthreads%% | Choose event count and simulation worker count independently of crate count. |
| Additional formats | Optional: include CSV/HIPO/etc. entries to request their normal output too. |

Only one SRO entry is supported per simulation. That implementation can accept payloads from several
compatible detector digitizers; it must understand all their payload types and use a common crate namespace.

%%implementation: example_sro%% resolves to `example_sro.gplugin` through %%plugin_path%% / %%GEMC_PLUGIN_PATH%%
and GEMC's normal library search. It is not named `gstreamer_example_sro_plugin.gplugin`. A library may export
both `GDynamicDigitizationFactory` and `GSROImplementationFactory`, as FT-Cal and the simple example do.

## Event workers and crate threads

{% include figure.html
src="assets/images/documentation/sro_flow.svg"
link="assets/images/documentation/sro_flow.svg"
alt="Event worker threads dispatch payloads to crate queues; progress acknowledgments establish safe time"
caption="Solid arrows carry payloads or show lifecycle order. Dashed arrows carry completion and timing
metadata. Each crate thread owns its queue consumption, frame processor, and output sink. Click to enlarge."
%}

Here, a worker means a Geant4 simulation thread processing an event; a crate thread is a separate output
collector.

1. The run owner calls %%begin_run%% before event processing. The selected implementation's
   %%configure_run%% supplies the timing model and memory limits. No crate files exist until requested.
2. Each worker's %%EndOfEventAction%% calls %%stream_hit%% for the applicable detector hits. The digitizer
   looks up electronics addresses, constructs an owned payload, and calls %%emit%% immediately.
3. GEMC's %%emit%% callback assigns an event-local sequence number and calls
   %%dispatch_payload_to_crate%%. That calls %%create_crate_thread_if_needed%% on first use and enqueues
   directly to the selected crate. Payloads bypass the master and the progress thread.
4. The crate thread creates its processor and sink, retains payloads in its ordering buffer, and acknowledges
   their delivery. Retention is not yet processing or a durable file write.
5. After its last dispatch, the worker calls %%complete_event%% through GEMC's event action, including for
   empty events. A separate progress thread combines closed events with crate acknowledgments and asks
   `GSROTiming` for a proven lower bound on all remaining input times.
6. Each crate releases payloads strictly before that boundary in %%(time, event_id, sequence)%% order. It calls
   %%consume_payload%%, then %%advance_time%%; the processor writes frames it can now prove complete.
7. After event workers return, the run owner drains accepted input, finalizes and joins crate threads.
   The processor's %%finish_run%% decides the unfinished-frame policy; %%finish_output%% checks file closure.

Worker scheduling may deliver later events first. There is no worker-side frame buffer: unfinished frames
belong to crate processors. Dispatch can wait for bounded queue space, so a slow writer can still slow the
simulation. The master performs lifecycle coordination without collecting every worker's frame data.

A detector's default %%stream_hit%% emits nothing. The current event action also skips detectors selected by
%%no_dgt%%. SRO reads accumulated `GHit` objects before the ordinary digitization pass; normal output threshold
and efficiency hooks do not automatically filter SRO payloads. Define the relevant response in the SRO path.

## Event time and frame completeness

An **event** is one simulated interaction. A **frame** collects signals that fall within a chosen time
interval. It can contain signals from several events, and one event can send signals to several frames.
The signal time determines the frame, regardless of which worker finishes first.

%%eventTimeWidth%% sets the spacing between event starts on the readout timeline. With
%%eventTimeWidth: 10*ns%%, event 0 starts at 0 ns, event 1 at 10 ns, event 2 at 20 ns, and so on.
It does **not** mean that every signal from an event must arrive within those 10 ns.

A detector plugin can add particle travel time and detector or electronics delays to the event start:

```text
signal time = event start + time of the signal relative to that event
```

For example, suppose frames are 40 ns long and event 3 starts at 30 ns:

| Signal from event 3 | Time after event start | Signal time | Destination |
|---|---|---|---|
| First hit | 5 ns | 35 ns | Frame 0: from 0 ns up to, but not including, 40 ns. |
| Second hit | 15 ns | 45 ns | Frame 1: from 40 ns up to, but not including, 80 ns. |

Both hits belong to the same simulation event, but they belong to different readout frames. A signal at
exactly 40 ns goes into frame 1. The frame processor uses the time supplied by the worker to make this choice.

The random-ADC example deliberately uses a simpler model: **every sample gets its event's start time**.
It does not add the geantino's travel time. All samples from event 3 therefore have time 30 ns in that
example. This keeps the example focused on moving samples between workers and crate threads. A detector
plugin that models signal delays can produce the 35 ns and 45 ns samples shown above.

### The timing contract

**The frame duration in this example is 40 ns.** The plugin defines it as %%frame_duration{40}%% in
`sro_payload.h`. It is separate from %%eventTimeWidth: 10*ns%%, which spaces event starts 10 ns apart.
Other plugins can choose a different frame duration; 40 ns is not a GEMC requirement.

| Frame | Start time, included | End time, excluded | Duration |
|---|---|---|---|
| 0 | 0 ns | 40 ns | 40 ns |
| 1 | 40 ns | 80 ns | 40 ns |
| 2 | 80 ns | 120 ns | 40 ns |

A frame's **end time** is the boundary we compare with %%safe_time%%. For frame 1, that end time is 80 ns,
although its duration is 40 ns. %%safe_time%% changes as the run progresses; it is not the frame duration
and need not be a multiple of 40 ns.

The next question is: **when does a crate know that it has received every sample needed for a frame?**
Seeing a sample in a later frame is not enough. For example, after receiving a sample at 45 ns, the crate
could still be waiting for another worker to send a sample at 35 ns. Writing frame 0 immediately would
leave that sample out.

`Timing` answers a specific question for GEMC: **what is the earliest time any sample still to come could
have?** We call the answer %%safe_time%%. If the answer is 40 ns, no sample still to come can belong before
40 ns. Once the crate has processed the samples it already holds before 40 ns, it can close frame 0.

For a model where signals cannot occur before their event starts, the steps are:

1. Event 3 starts at 30 ns. While its worker is still running, it could still send the 35 ns sample.
   Frame 0 must wait, even if events 4 or 5 have already finished on other workers.
2. GEMC checks that **all** events 0–3 have finished and all their samples have reached their destination
   crate buffers. This includes event 3's 45 ns sample, even though it belongs to a later frame.
3. The first event whose samples might still arrive is event 4, starting at 40 ns. `Timing` can therefore
   return 40 ns: every sample still to come must have a time of 40 ns or later.
4. The crate processes its samples before 40 ns and writes frame 0. The 45 ns sample remains in frame 1;
   that frame needs a later %%safe_time%% of at least 80 ns before it can be written.

So there are two related rules: **a sample's time chooses its frame; the timing guarantee tells the crate
when that frame can be closed.** The guarantee is about simulation signal times, not how long a worker
has taken to run, and not the latest sample time seen so far.

#### Positive and negative timing corrections

Consider **event 6**, which starts at %%6 * 10 ns = 60 ns%%. To isolate the effect of a correction, assume
its uncorrected hit times are at that event start: there is no extra travel or detector delay in this table.
Positive corrections move a hit later; negative corrections move it earlier on the readout timeline.

```text
corrected signal time = 60 ns + correction
```

| Correction | Corrected signal time | Destination frame |
|---|---|---|
| +5 ns | 65 ns | Frame 1: 40–80 ns. |
| +15 ns | 75 ns | Frame 1: 40–80 ns. |
| +25 ns | 85 ns | Frame 2: 80–120 ns. |
| −5 ns | 55 ns | Frame 1: 40–80 ns. |
| −15 ns | 45 ns | Frame 1: 40–80 ns. |
| −25 ns | 35 ns | Frame 0: 0–40 ns. |

The same event can therefore contribute to an earlier frame, its event-start frame, and a later frame.
These are corrected signal timestamps; a negative correction does not mean the particle travels backwards.
In a real detector, include the hit time, travel or propagation delay, and calibration corrections when
calculating the **total offset from the event start**. The guarantee must cover that total offset, not just
one correction term. The shipped random-ADC example has zero offsets; this table illustrates an extension.

Now suppose event 6 is the first event whose samples might still arrive. What can `Timing` promise?

| Offsets allowed by the model | Earliest possible offset | Returned %%safe_time%% |
|---|---|---|
| Only +5, +15, or +25 ns | +5 ns | 60 + 5 = 65 ns. |
| Any of the six corrections above | −25 ns | 60 − 25 = 35 ns. |

With only the positive offsets, all remaining samples must be at 65 ns or later. After processing its
buffered samples before 65 ns, the crate can close frame 0, whose end is 40 ns. It cannot yet close frame 1,
whose end is 80 ns.

With the negative offsets also allowed, event 6 could still send the 35 ns sample. Frame 0 must stay open.
Once GEMC confirms that events 0–6 and their sample deliveries are finished, event 7 is the first event
still to come. Its start is 70 ns, so the earliest remaining signal is %%70 - 25 = 45 ns%%. After processing
samples before 45 ns, the crate can close frame 0.

#### Exactly what the plugin author implements

**Implement %%GSROTiming::earliest_remaining_time(...)%%. %%safe_time%% is the value it returns, not a
separate callback or a YAML option that the user sets.** GEMC calls this method with
%%first_undelivered_event%%: the first event for which completion and delivery of all samples have not yet
both been confirmed. GEMC does that bookkeeping; the plugin does not count finished workers or events itself.

For events spaced by a fixed %%eventTimeWidth%%, your method returns:

```text
safe_time = first_undelivered_event * eventTimeWidth + minimum_signal_time
```

Here %%minimum_signal_time%% means the earliest total signal offset your model allows, for **any channel
of any crate and any remaining event**. For the six-correction model above, it is −25 ns. It must be a
reliable limit of the model, not the smallest value observed in the samples received so far. A value earlier
than necessary is safe but delays output; a value later than a possible remaining sample is incorrect.

For that model, a timing class could be:

```cpp
// Illustrative extension of the example's Timing class: allow a minimum total signal offset.
class OffsetTiming final : public GSROTiming {
public:
    OffsetTiming(GSROTime width, GSROTime minimum_signal_time)
        : width(width), minimum_signal_time(minimum_signal_time) {}

    std::optional<GSROTime> earliest_remaining_time(GSROEventId first_undelivered_event) const override {
        // GEMC supplies the first event whose samples might still arrive.
        const auto event_start = width * static_cast<std::int64_t>(first_undelivered_event);
        // No sample from this event OR ANY LATER EVENT may have a time before this result.
        return event_start + minimum_signal_time;
    }

private:
    GSROTime width;
    GSROTime minimum_signal_time;
};
```

Your %%GSROImplementation::configure_run%% returns this timing object as part of `GSROConfiguration`.
For the numerical example, its return statement would be:

```cpp
// 10 ns between event starts; no emitted sample can be earlier than event_start - 25 ns.
// {} keeps the default crate limits; 65536 is the pending-event bookkeeping limit.
return {std::make_shared<OffsetTiming>(GSROTime{10}, GSROTime{-25}), {}, 65536};
```

These hard-coded numbers explain the model. A configurable implementation should read and validate its
event width and timing limits in %%configure_run%%, as the shipped example already does for the width.

There are three parts of the plugin to keep consistent:

1. **Worker — %%stream_hit%%:** calculate each corrected signal time and supply it to %%emit%%. The worker's
   signal model must respect the minimum promised by `Timing`; validate it or guarantee it by construction.
2. **Timing — %%earliest_remaining_time%%:** return the earliest possible remaining signal time. The shipped
   zero-offset example returns %%event_start%%; the six-correction extension returns %%event_start - 25 ns%%.
3. **Crate processor — %%advance_time(GSROTime safe_time)%%:** use the value GEMC passes in. GEMC first calls
   %%consume_payload%% for all buffered samples before that time. The processor can then write frames whose
   **end time** is at or before %%safe_time%%. It does not calculate a new guarantee from the latest hit.

The returned time must never move backwards as GEMC confirms more events. Return %%std::nullopt%% if no
earliest time can be guaranteed. GEMC will then keep waiting to process buffered samples in time order;
continued buffering can eventually reach the configured memory limits.

A simple frame processor can write %%[begin, end)%% when %%end <= safe_time%%, after processing all samples
before that time. GEMC holds samples exactly at %%safe_time%% until the guarantee moves forward.
If electronics processing still has an unresolved pulse or overlap, the plugin may need to wait longer.
Keep any such state across frame boundaries.

Stopping the simulation does not automatically make the final frame complete. GEMC passes the last
%%safe_time%% and the completion or interruption reason in `GSROEndContext`. It delivers the remaining
submitted samples before calling %%finish_run%%, and the plugin decides what to do with unfinished frames.
The example discards them. With ten events spaced by 10 ns, its final %%safe_time%% is 100 ns: it writes
frames ending at 40 and 80 ns, but discards the unfinished frame ending at 120 ns.

### Where the event clock is defined

%%eventTimeWidth%% belongs to the `gparticle` module. Plugins read it through
%%gparticle::getEventTimeWidth(options)%% in `gemc/gparticle/gparticle_options.h`, in Geant4 internal time
units. The default %%0*ns%% requests no continuous timeline. FT-Cal and the example require a positive
whole number of nanoseconds. Event IDs restart at zero for each run invocation.

This setting is separate from the `GReadoutSpecs` window that groups Geant4 steps into hits and from the
output frame duration. It does not itself change Geant4 primary-vertex times. `GSROEventContext` currently
contains %%run_id%% and %%event_id%% only. Support for explicit event timestamps or uneven event spacing is
a future extension; such a model would also need a reliable earliest time for samples still to come.

## Define a streaming implementation

Keep electronics-specific code in the owning experiment repository, such as `clas12-systems`. Use the GEMC
[source example](https://github.com/gemc/src/tree/main/examples/basic/sro) as a small complete implementation.

### Worker payload and translation table

Derive your data classes from `GSROData`. `GSROPayload` is GEMC's transport envelope, not the payload base
class. It contains the crate, event ID, sequence, absolute simulation time, and owned data. `GSROFrame` is the
corresponding envelope for a completed frame with a crate, frame ID, interval, and owned contents.

The example uses `AdcPayload` for one sample and `AdcFrame` for a vector of samples; both are shown below.
Payloads must own their contents and must not retain pointers into a `GHit`, event collection, or mutable
worker state. After %%emit%% transfers ownership, retain no mutable aliases and do not store the callback.

The example's `Digitizer` fills the inherited %%translationTable%% in %%loadTTImpl%% before the run, then
resolves %%hit->getTTID()%% in %%stream_hit%%. Keys must match the sensitive identifiers and their order.
These methods come from
[`sro_plugin.cc`](https://github.com/gemc/src/blob/main/examples/basic/sro/sro_plugin.cc):

```cpp
class Digitizer final : public GDynamicDigitization {
public:
    using GDynamicDigitization::GDynamicDigitization;
    bool loadTTImpl([[maybe_unused]] int runno, [[maybe_unused]] const std::string& variation) override {
        // GEMC calls this before the run. This example's mapping is independent of run/variation.
        // Keys match the sensitive IDs in sro.py; only this table defines the hardware addresses.
        auto table = std::make_shared<GTranslationTable>(gopts);
        using Mode = GElectronic::ComparisonMode;
        table->addGElectronicWithIdentity({101}, GElectronic(1, 3, 0, Mode::crate_slot_channel));
        table->addGElectronicWithIdentity({102}, GElectronic(1, 3, 1, Mode::crate_slot_channel));
        table->addGElectronicWithIdentity({103}, GElectronic(2, 3, 0, Mode::crate_slot_channel));
        table->addGElectronicWithIdentity({104}, GElectronic(2, 3, 1, Mode::crate_slot_channel));
        // Publish through the inherited member; workers only read the completed table during the run.
        translationTable = std::move(table);
        return true;
    }
    bool defineReadoutSpecsImpl() override {
        // Group steps within a plane into one hit. This Geant4 hit window is independent of SRO frames.
        readoutSpecs = std::make_shared<GReadoutSpecs>(1000 * CLHEP::ns, 0, 1 * CLHEP::cm, log);
        return true;
    }
    void stream_hit(GHit* hit, std::size_t, const GSROEventContext& event,
                    const GSROEmit& emit) const override {
        if (!translationTable) { throw std::logic_error("SRO translation table was not loaded"); }
        // getTTID() returns the sensitive identity vector. Missing entries fail in getElectronics().
        const auto address = translationTable->getElectronics(hit->getTTID()).getHAddress();
        AdcSample sample{static_cast<std::uint32_t>(address[0]), static_cast<std::uint32_t>(address[1]),
                         static_cast<std::uint32_t>(address[2]), 0};
        // Local RNG, seeded from the address and event: reproducible across worker schedules, with no
        // shared random state and no changes to the simulation's physics RNG. This is a toy ADC model.
        std::seed_seq seed{12345u, static_cast<std::uint32_t>(event.event_id),
                           sample.crate, sample.slot, sample.channel};
        std::mt19937 random(seed);
        sample.adc = std::uniform_int_distribution<std::uint32_t>(0, 4095)(random);
        const auto event_width = gparticle::getEventTimeWidth(gopts);
        if (event_width <= 0 || std::floor(event_width) != event_width) {
            throw std::invalid_argument("SRO example requires a positive integral eventTimeWidth");
        }
        const auto time = GSROTime{static_cast<std::int64_t>(event_width)} *
                          static_cast<std::int64_t>(event.event_id);
        emit(sample.crate, time, std::make_unique<AdcPayload>(sample));
    }
};
```

%%defineReadoutSpecsImpl%% groups Geant4 steps into hits. That integration window is independent of the
40 ns SRO frames. %%stream_hit%% uses the translation table's crate, slot, and channel, samples a local RNG,
and transfers the result immediately. GEMC creates and routes the envelope; the digitizer manages no threads.

### Required objects and callbacks

Each entry below uses the actual random-ADC example, with comments explaining ownership and callback purpose.
The snippets belong to the %%simple_sro%% namespace; include lists are omitted here. The complete files are
[`sro_payload.h`](https://github.com/gemc/src/blob/main/examples/basic/sro/sro_payload.h) and
[`sro_plugin.cc`](https://github.com/gemc/src/blob/main/examples/basic/sro/sro_plugin.cc).

| GEMC interface | Example implementation | Responsibility |
|---|---|---|
| `GSROData` | [AdcPayload and AdcFrame](#gsrodata-owned-samples-and-frames) | Own data; report memory. |
| `GSROTiming` | [Timing](#gsrotiming-prove-input-progress) | Bound every remaining payload's time. |
| `GSROImplementation` | [Implementation](#gsroimplementation-configure-and-create) | Set up crates. |
| `GSROCratePlugin` | [Crate](#gsrocrateplugin-assemble-complete-frames) | Collect, emit, and finalize frames. |
| `GSROFrameSink` | [CsvSink](#gsroframesink-write-and-close) | Encode frames and check file closure. |

#### GSROData: owned samples and frames

`AdcSample` is the plain record; the two derived classes own the data GEMC transports. The frame's memory
report includes vector capacity, since allocated storage can exceed the current sample count.

```cpp
// The entire example record: an electronics address and a 12-bit ADC count. These are values,
// not pointers into a hit or a digitizer. Crate is repeated in the transport envelope for routing.
// The worker obtains crate/slot/channel from the translation table populated by loadTTImpl.
struct AdcSample {
    std::uint32_t crate;   // 1 or 2 in this geometry.
    std::uint32_t slot;    // 3 in this geometry.
    std::uint32_t channel; // 0 or 1 in each crate.
    std::uint32_t adc;     // Uniform random integer in [0, 4095]; no energy calibration.
};

// A worker transfers one sample to its crate. GEMC supplies event_id and sequence in GSROPayload;
// its time field is separate from this experiment-defined record.
struct AdcPayload final : GSROData {
    explicit AdcPayload(AdcSample value) : sample(value) {}
    AdcSample sample;
    std::size_t size_bytes() const noexcept override { return sizeof(*this); }
};

// The crate combines samples from every worker/channel into one time frame. Only the crate thread
// modifies this vector. The sink receives ownership after the frame is proven complete.
struct AdcFrame final : GSROData {
    std::vector<AdcSample> samples;
    std::size_t size_bytes() const noexcept override {
        return sizeof(*this) + samples.capacity() * sizeof(AdcSample);
    }
};
```

#### GSROTiming: prove input progress

This is the code behind [the timing contract](#the-timing-contract). GEMC tells it the first event whose
samples might still arrive. In this example, event 4 starts at 40 ns and none of its samples can be earlier,
so %%first = 4%% and %%width = 10 ns%% give an answer of 40 ns. The answer must also cover every later event.
Update this calculation if the worker's signal model can produce earlier times.

```cpp
class Timing final : public GSROTiming {
public:
    explicit Timing(GSROTime width) : width(width) {}
    // No sample still to come, from first or any later event, can have an earlier time.
    std::optional<GSROTime> earliest_remaining_time(GSROEventId first) const override {
        return width * static_cast<std::int64_t>(first);
    }

private:
    GSROTime width;
};
```

#### GSROImplementation: configure and create

%%configure_run%% runs on the run owner before event processing. %%create_crate%% runs once on each lazily
created crate thread. Calls for different crates can overlap; this implementation keeps all mutable frame
and file state in the returned resources.

```cpp
class Implementation final : public GSROImplementation {
public:
    using GSROImplementation::GSROImplementation;
    // Validate the common event clock and return timing plus framework storage limits.
    GSROConfiguration configure_run(const GSRORunContext&) override {
        const auto width = gparticle::getEventTimeWidth(options);
        if (width <= 0 || std::floor(width) != width) {
            throw std::invalid_argument("SRO example requires a positive integral eventTimeWidth");
        }
        // {} selects default crate limits; 65536 bounds pending-event bookkeeping.
        return {std::make_shared<Timing>(GSROTime{static_cast<std::int64_t>(width)}), {}, 65536};
    }
    // Called on the new crate thread: open its file and attach its frame processor.
    GSROCrateResources create_crate(GSROCrateId id, const GSRORunContext& run) const override {
        auto sink = std::make_unique<CsvSink>(run.output_basename + "_r" + std::to_string(run.run_id) +
                                              "_crate" + std::to_string(id) + ".csv");
        auto crate = std::make_unique<Crate>(*sink, id);
        // Transfer both objects to GEMC. The sink outlives the processor that references it.
        return {std::move(sink), std::move(crate)};
    }
};
```

Export the actual factory below **outside** the %%simple_sro%% namespace. GEMC resolves this symbol from
%%example_sro.gplugin%%. The example also exports its separate digitization factory from the same library.

```cpp
// Construct the implementation selected by gstreamer.implementation.
extern "C" GSROImplementation* GSROImplementationFactory(const std::shared_ptr<GOptions>& options) {
    return new simple_sro::Implementation(options);
}
```

#### GSROCratePlugin: assemble complete frames

Only the owning crate thread touches %%frames%%. %%consume_payload%% collects input, %%advance_time%% emits
proven complete frames, and %%finish_run%% applies the example's discard policy to the remaining state.
The plugin imposes the 40 ns frame duration; GEMC imposes no frame size.

```cpp
inline constexpr GSROTime frame_duration{40}; // Nanoseconds; shared by every crate in this example.

class Crate final : public GSROCratePlugin {
public:
    Crate(GSROFrameSink& sink, GSROCrateId id) : GSROCratePlugin(sink), crate_id(id) {}
    // GEMC delivers records in (time, event_id, sequence) order. Retain them without writing yet.
    void consume_payload(GSROPayload payload) override {
        const auto& sample = dynamic_cast<const AdcPayload&>(*payload.data).sample;
        if (sample.crate != crate_id || payload.time < GSROTime{0}) {
            throw std::invalid_argument("Unexpected crate or negative time in the simple SRO example");
        }
        const auto frame_id = static_cast<std::uint64_t>(payload.time / frame_duration);
        auto& frame = frames[frame_id];
        if (!frame) { frame = std::make_unique<AdcFrame>(); }
        frame->samples.push_back(sample);
    }
    // All payloads earlier than safe_time have been consumed; complete frames may now be written.
    void advance_time(GSROTime safe_time) override {
        while (!frames.empty()) {
            const auto id = frames.begin()->first;
            const auto begin = frame_duration * static_cast<std::int64_t>(id);
            const auto end = begin + frame_duration;
            if (end > safe_time) { break; } // A payload exactly at end belongs to the NEXT frame.
            auto frame = frames.extract(frames.begin());
            output.write_frame({crate_id, id, begin, end, std::move(frame.mapped())});
        }
    }
    void finish_run(const GSROEndContext&) override {
        // GEMC has delivered the remaining input, but it has not declared that input complete.
        // This implementation discards unfinished frames, including any unproven tail after interruption.
        frames.clear();
    }
private:
    GSROCrateId crate_id;
    std::map<std::uint64_t, std::unique_ptr<AdcFrame>> frames;
};
```

At shutdown, GEMC also consumes the remaining submitted records beyond the last proven boundary. They may
populate incomplete frames, so %%consume_payload%% must not equate arrival with completeness. The example's
%%finish_run%% clears them on both completion and interruption; another implementation may inspect
%%GSROEndContext::reason%% and %%safe_time%% to implement a different explicit policy.

#### GSROFrameSink: write and close

The sink accepts ownership of each completed frame and serializes its samples. Construction, writes, and
checked closure all happen on the crate thread. Enabling stream exceptions makes I/O failures visible to GEMC.

```cpp
class CsvSink final : public GSROFrameSink {
public:
    explicit CsvSink(const std::string& filename) {
        file.exceptions(std::ios::failbit | std::ios::badbit); // Report open/write/close failures to GEMC.
        file.open(filename);
        file << "frame_id,begin_ns,end_ns,crate,slot,channel,adc\n";
    }
    // Take ownership of a complete frame and encode one CSV row per sample.
    void write_frame(GSROFrame frame) override {
        const auto& data = dynamic_cast<const AdcFrame&>(*frame.data);
        for (const auto& sample : data.samples) {
            file << frame.frame_id << ',' << frame.begin.count() << ',' << frame.end.count() << ','
                 << sample.crate << ',' << sample.slot << ',' << sample.channel << ',' << sample.adc << '\n';
        }
    }
    // Checked flush/close: destruction alone cannot report an output failure to the run owner.
    void finish_output() override { file.close(); }
private:
    std::ofstream file;
};
```

### The callback lifecycle

The diagram follows the example's callbacks for one crate. Each active crate has its own independent copy
of this sequence. The existing [thread diagram](#event-workers-and-crate-threads) shows payload routing
between event workers, progress tracking, and multiple crates.

{% include figure.html
src="assets/images/documentation/sro_lifecycle.svg"
link="assets/images/documentation/sro_lifecycle.svg"
alt="SRO callbacks from run configuration through crate creation, safe-time processing, and checked shutdown"
caption="Callbacks execute on the named thread. The loop writes only complete frames; orderly shutdown drains
remaining input before discarding the example's unfinished frames and closing its sink. Click to enlarge."
%}

1. **Run owner:** %%configure_run%% validates options and supplies the timing model and limits.
2. **Event workers:** %%stream_hit%% resolves the TT address and calls %%emit%%. First dispatch to a crate
   starts its collector; that crate thread calls %%create_crate%% to construct its sink and processor.
3. **Progress thread:** %%earliest_remaining_time%% supplies a safe boundary from the fully delivered event
   prefix. It can be queried before any crate exists; a new crate receives the current bound when available.
4. **Crate thread, repeated:** retain incoming payloads, then call %%consume_payload%% for all records
   strictly before a safe boundary in sorted order. Call %%advance_time%% after consuming them; the example
   invokes %%write_frame%% for every occupied frame whose end is at or before that boundary.
5. **Crate thread, orderly shutdown:** drain accepted messages and apply any newer final safe boundary.
   Consume remaining submitted records in order, then call %%finish_run%% and %%finish_output%% once each.
   Destroy the processor before the sink; the run owner joins the thread. An interrupted run uses this same
   path with %%reason: interrupted%% and the last proven boundary, not an infinite cutoff.

All processor and sink callbacks, resource construction, and destruction occur on the owning crate thread.
GEMC retains the implementation library until its objects are destroyed. The timing callback must be
thread-safe, prompt, and must not call back into the service. After a callback throws, GEMC cancels input,
wakes blocked producers, and joins threads before reporting the error; successful finalization callbacks
are not guaranteed on that failure path.

### Decisions the implementation author must make

These are contracts to implement even if the chosen policy is simple:

| Decision | What must be defined |
|---|---|
| Payload schema | Types, units, valid ranges, ownership, and destination crate. |
| Translation | Sensitive-ID keys and the electronics table source. |
| Time model | Common run origin, event mapping, signal offsets, and safe-time proof. |
| Frame model | IDs, %%[begin, end)%% boundaries, duration, and readiness rules. |
| Output | Encoding, per-crate destination, filename policy, and checked close. |
| End of input | Treatment of partial frames on completion and interruption. |
| Retained state | Limits for frame/electronics memory that GEMC cannot account for. |

The implementation **may choose** integral samples or waveforms; independent contributions or overlap
merging; dead time, thresholds, and saturation; empty-frame emission or omission; and discard, marked partial
output, or another explicit tail policy. Overlap modeling is optional. The crate processor already provides
its hook; a separate overlap-plugin API has not been introduced.

These choices may be fixed in C++ or exposed as experiment options. GEMC has no generic YAML %%frame_duration%%,
%%overlap%%, or %%write_partial_frames%% setting. A plugin must register any such option itself. Declare options
through %%definePluginOptions%% in a startup-discovered library; see
[option discovery](/home/documentation/sensitivity/gplugins/#runtime-digitization-and-startup-option-discovery).
For FT, `ft.gplugin` registers the options for the runtime detector libraries.

### Why crate limits are separate

`GSROCrateLimits` bounds framework storage per crate. These are C++ configuration fields, not automatically
available YAML keys:

| Field | Default | Behavior at the limit |
|---|---|---|
| %%queue_messages%% | 1024 | Producer waits for queue space. |
| %%queue_bytes%% | 4 MiB | Producer waits; a payload too large to fit is rejected. |
| %%pending_payloads%% | 65536 | Exceeding the ordering-buffer limit fails the run. |
| %%pending_bytes%% | 64 MiB | Exceeding the ordering-buffer limit fails the run. |

A queue can drain while an early event still prevents ordered delivery. Its records then accumulate in a
separate pending buffer. Blocking that crate at the pending limit could prevent the earlier payload or
progress message needed to unblock it, so overflow is an error. Counts bound many tiny records; byte limits
account for the envelope plus %%data->size_bytes()%%. They exclude allocator overhead, producer-held objects,
and state retained by the plugin, and therefore are not a total process-memory budget.

%%GSROConfiguration::max_pending_events%% defaults to 65536 and bounds event-progress bookkeeping, including
empty events behind an unfinished event. Exceeding it also fails instead of blocking the missing event's
worker. All limits must be positive. The shipped implementations use the defaults; authors can tune them.

Background errors cancel input to all crates, wake blocked producers, and are reported after threads are
joined. Normal %%finish_run%%/%%finish_output%% success is not guaranteed after an exception; destructors still
release resources. Callbacks must terminate because joining cannot interrupt a hung plugin or output call.

## Simple random-ADC example

The GEMC example uses four scoring planes, with sensitive IDs mapped in %%loadTTImpl%%:

| Sensitive ID | Crate | Slot | Channel |
|---|---|---|---|
| 101 | 1 | 3 | 0 |
| 102 | 1 | 3 | 1 |
| 103 | 2 | 3 | 0 |
| 104 | 2 | 3 | 1 |

Each worker resolves the table and produces a 12-bit random ADC. The RNG uses event/address seeds local to
the example, independent of the physics RNG; identical input is reproducible across worker schedules on the
same C++ toolchain. There is no flight-time offset, calibration, overlap, or dead time in this example.

With %%eventTimeWidth: 10*ns%% and a 40 ns frame, ten events produce:

| Frame | Interval | Events | Result per crate |
|---|---|---|---|
| 0 | [0, 40) ns | 0–3 | 8 samples written. |
| 1 | [40, 80) ns | 4–7 | 8 samples written. |
| 2 | [80, 120) ns | 8–9 | Discarded; final safe time is 100 ns. |

The files are %%simple_sro_r1_crate1.csv%% and %%simple_sro_r1_crate2.csv%%, with columns
%%frame_id,begin_ns,end_ns,crate,slot,channel,adc%%. A sample at 40 ns belongs to frame 1.

With the Geant4 build environment loaded, compile and check it from the GEMC source repository:

```sh
meson compile -C build gemc example_sro
meson test -C build examples_sro_adc --print-errorlogs
```

The [example README](https://github.com/gemc/src/blob/main/examples/basic/sro/README.md) includes commands to
produce geometry and run in a scratch directory. The test exercises real geometry, TT lookup, plugin loading,
crate output, one/four workers, exact boundaries, and unfinished-frame discard.

## FT-Cal implementation and current scope

The `clas12-systems` implementation uses the preserved JLAB SRO integral definitions. Its worker loads the
FT-Cal translation table through %%loadTTImpl%% and resolves addresses with %%getTTID()%%. Column 5 is the
crystal number; the key matches the geometry's two coordinate identifiers:

```cpp
const int ix = crystal % 22 + 1;
const int iy = crystal / 22 + 1;
table->addGElectronicWithIdentity({ix, iy},
    GElectronic(crate, slot, channel, GElectronic::ComparisonMode::crate));
```

The source is %%/daq/tt/ftcal:1%%, retaining the reference-run TT convention. Columns 0–2 provide crate, slot,
and channel. %%ComparisonMode::crate%% is the modern form of mode 0: crate is the frame source and the stored
address still includes slot/channel. The frame processor collects all mapped channels of that crate.

FT-Cal currently defines the following policies:

- One calibrated integral per accumulated Geant4 hit; zero-energy hits emit nothing. Hardware-disabled
  channels are skipped when %%ft_cal_accountForHardwareStatus%% is enabled.
- Charge follows the detector energy-to-ADC conversion, truncates to an integer, and saturates at 8191.
- Signal time includes average hit time, crystal propagation, calibration offset, and Gaussian smearing.
  It is floored to integral ns and added to %%event_id * eventTimeWidth%%. Signals before acquisition are
  discarded.
- %%ft_cal_sro_min_signal_time%% defaults to -1000 ns and is an enforced lower bound on event-relative time.
  A violation fails the run; Gaussian tails are not silently clamped. Set this bound for your source and
  calibrations. Both it and %%eventTimeWidth%% must be integral ns; width is in [1, 1e12], bound in [-1e12, 0].
- Frames are 65,536 ns, with integral time encoded in 4 ns ticks. Complete occupied frames are written;
  empty frames are omitted and unfinished frames discarded on normal or interrupted shutdown.
- Contributions remain separate across hits/events. Pulse sampling, overlap merging, and dead time are
  future detector work. Frame duration and those policies are currently fixed in C++, not user options.

A short FT run may therefore write only the preamble. With %%eventTimeWidth: 10*ns%% and the default -1000 ns
bound, the final safe time after %%N%% delivered events is %%N * 10 ns - 1000 ns%%. The first frame ends at
65,536 ns, requiring at least 6654 fully delivered events to prove complete. It is written only if occupied.

See [JLAB SRO Output](/home/documentation/output/jlabsro/) for binary fields, limits, and migration from
%%format: jlabsro%%. The required `DataFrameHeader` and setup/serialization helpers are ported into
`clas12-systems/geometry_src/sro/daq`. Its README records the original sources and port decisions. Obsolete
source copies have been removed, including the `JLABSRO` directory from the GEMC framework.

## Validation and remaining work

GEMC's SRO tests cover concurrent producers, ordering and limits, delivery tracking, background failures,
serial/multithreaded runtime integration, empty events, repeated invocations, and the full random-ADC example:

```sh
meson test -C build --suite sro --print-errorlogs
```

In a matching `clas12-systems` build, the SRO suite includes %%test_sro_jlab_format%% and
%%sro_ftcal_full_path%%. They check byte fixtures, address/time/charge ranges, slot directory limits, frame
boundaries, interrupted tails, and synthetic local CCDB-to-TT-to-worker-to-binary output with one/four workers.
The fixtures run offline. Production FT-Cal CCDB assignments and compatibility with a production JLAB reader
still need validation; local format tests do not establish that compatibility.
