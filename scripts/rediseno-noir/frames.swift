import AVFoundation
import AppKit
let args = CommandLine.arguments
let path = args[1], outDir = args[2], n = Int(args[3]) ?? 12
let asset = AVURLAsset(url: URL(fileURLWithPath: path))
let dur = CMTimeGetSeconds(asset.duration)
let gen = AVAssetImageGenerator(asset: asset)
gen.appliesPreferredTrackTransform = true
gen.requestedTimeToleranceBefore = .zero; gen.requestedTimeToleranceAfter = .zero
gen.maximumSize = CGSize(width: 360, height: 640)
print("duración", dur)
for i in 0..<n {
  let t = CMTimeMakeWithSeconds(dur * (Double(i) + 0.5) / Double(n), preferredTimescale: 600)
  do {
    let cg = try gen.copyCGImage(at: t, actualTime: nil)
    let rep = NSBitmapImageRep(cgImage: cg)
    if let data = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.8]) {
      try data.write(to: URL(fileURLWithPath: "\(outDir)/f\(String(format: "%02d", i)).jpg"))
    }
  } catch { print("frame", i, "error", error) }
}
