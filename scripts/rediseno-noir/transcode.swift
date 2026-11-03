import AVFoundation
import Foundation
// Recomprime un MP4 a H.264 + AAC con el tamaño y el bitrate que se le pidan (como ffmpeg, pero con lo que trae la Mac).
let a = CommandLine.arguments
let src = URL(fileURLWithPath: a[1]), dst = URL(fileURLWithPath: a[2])
let outW = Int(a[3])!, outH = Int(a[4])!, vbr = Int(a[5])!, abr = Int(a[6])!
try? FileManager.default.removeItem(at: dst)
let asset = AVURLAsset(url: src)
let reader = try! AVAssetReader(asset: asset)
let writer = try! AVAssetWriter(outputURL: dst, fileType: .mp4)
let vTrack = asset.tracks(withMediaType: .video).first!
let aTrack = asset.tracks(withMediaType: .audio).first
let vOut = AVAssetReaderTrackOutput(track: vTrack, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange])
reader.add(vOut)
let vIn = AVAssetWriterInput(mediaType: .video, outputSettings: [
  AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: outW, AVVideoHeightKey: outH,
  AVVideoScalingModeKey: AVVideoScalingModeResizeAspectFill,
  AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: vbr, AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel, AVVideoMaxKeyFrameIntervalKey: 60]])
vIn.transform = vTrack.preferredTransform
writer.add(vIn)
var aIn: AVAssetWriterInput? = nil, aOut: AVAssetReaderTrackOutput? = nil
if let t = aTrack {
  let o = AVAssetReaderTrackOutput(track: t, outputSettings: [AVFormatIDKey: kAudioFormatLinearPCM])
  reader.add(o); aOut = o
  let i = AVAssetWriterInput(mediaType: .audio, outputSettings: [AVFormatIDKey: kAudioFormatMPEG4AAC, AVNumberOfChannelsKey: 2, AVSampleRateKey: 44100, AVEncoderBitRateKey: abr])
  writer.add(i); aIn = i
}
writer.shouldOptimizeForNetworkUse = true
writer.startWriting(); reader.startReading(); writer.startSession(atSourceTime: .zero)
let g = DispatchGroup()
func pump(_ input: AVAssetWriterInput, _ output: AVAssetReaderTrackOutput) {
  g.enter()
  input.requestMediaDataWhenReady(on: DispatchQueue(label: input.mediaType.rawValue)) {
    while input.isReadyForMoreMediaData {
      if let sb = output.copyNextSampleBuffer() { input.append(sb) } else { input.markAsFinished(); g.leave(); return }
    }
  }
}
pump(vIn, vOut); if let i = aIn, let o = aOut { pump(i, o) }
g.wait()
let sem = DispatchSemaphore(value: 0)
writer.finishWriting { sem.signal() }; sem.wait()
print("estado", writer.status.rawValue, writer.error.map { "\($0)" } ?? "ok")
